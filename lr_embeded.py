#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
#
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
#
##########################################################################
"""
@File    : lr_embeded.py
@Author  : chenghanni@baidu.com
"""
import os
import sys

sys.path.append(os.path.join(os.getcwd()))
import pandas as pd
from sklearn.linear_model import LogisticRegression
from pyspark.sql import SparkSession
from utils.model_train_log import logger

num_per_partition = 20000
invalid = False
msg = "SUCCESS"


def run(rdd, columns, lr_params, **kwargs):
    label_name = kwargs.get("labelName")
    param = kwargs.get("param", {})
    data = pd.DataFrame(list(rdd))
    data.columns = columns
    pre_count = len(data.index)
    data = data[data[label_name].notnull()]
    after_count = len(data.index)
    # logger.info('Delete %d rows whose label is null.' % (after_count - pre_count))
    label = data[label_name].astype(float)
    features = data.drop([label_name], axis=1).astype(float)
    features = features.fillna(0)
    lr = LogisticRegression(penalty=lr_params['penalty'],
                            class_weight=lr_params['class_weight'],
                            max_iter=lr_params['max_iter'], C=lr_params['C'],
                            tol=lr_params['C'],
                            fit_intercept=lr_params['fit_intercept']) \
        .fit(features, label)
    importance = zip(features.columns.tolist(), lr.coef_.tolist()[0])
    return importance


def arg_check(param):
    logger.info("Start to check args")
    global invalid
    global msg
    input_path = param.get("inputPath")
    delimiter = param.get("delimiter")
    label_name = param.get("labelName")
    if label_name is "" or None:
        invalid = True
        msg = "INVALID PARAMETER"
        logger.error("Error: invalid parameter label_name")
        return
    if input_path is None or "":
        invalid = True
        msg = "INVALID PARAMETER"
        logger.error("Error: invalid parameter inputPath")
        return
    if delimiter is None or "":
        invalid = True
        msg = "INVALID PARAMETER"
        logger.error("Error: invalid parameter delimeter")
        return


def prepare_lr_params(lr_params):
    logger.info("Start to prepare lr params.")
    default_lr_params = {'C': 1, 'tol': 1e-4,
                         'class_weight': {0: 1, 1: 1},
                         'fit_intercept': True,
                         'max_iter': 100,
                         'penalty': 'l2'}
    for k in default_lr_params:
        if k == 'class_weight':
            lr_params[k] = lr_params.get(k, default_lr_params[k])
        elif k == 'fit_intercept':
            lr_params[k] = lr_params.get(k, default_lr_params[k])
        elif k == 'penalty':
            lr_params[k] = lr_params.get(k, default_lr_params[k])
        elif k in ['C', 'max_iter']:
            lr_params[k] = int(lr_params.get(k, default_lr_params[k]))
        else:
            lr_params[k] = float(lr_params.get(k, default_lr_params[k]))
    logger.info('Lr params preparation finished.')
    return lr_params


def load_data(sparksession, input_path, schema_path, delimiter):
    logger.info("Start to load data")
    global invalid
    global msg
    if schema_path is None or "":
        try:
            data = sparksession.read.option(
                "delimiter", delimiter).option(
                "header", "true").option(
                "inferschema", "true").option(
                "mode", "DROPMALFORMED").csv(input_path)
            logger.info("Data ready.")
            return data, data.columns
        except:
            logger.error("Error: invalid input path or data type.")
            invalid = True
            msg = "INVALID DATA"
            return None
    else:
        try:
            data = sparksession.read.option(
                "delimiter", delimiter).option(
                "header", "false").option(
                "inferschema", "true").option(
                "mode", "DROPMALFORMED").csv(input_path)
            logger.info("Data ready.")
        except:
            logger.error("Error: invalid input path or data type.")
            invalid = True
            msg = "INVALID DATA"
            return None
        try:
            schema = sparksession.read.option(
                "delimiter", delimiter).option(
                "header", "true").option(
                "inferschema", "true").option(
                "mode", "DROPMALFORMED").csv(schema_path)
        except:
            logger.error("Error: invalid input path or data type.")
            invalid = True
            msg = "INVALID DATA"
            return None
        if len(data.columns) != len(schema.columns):
            logger.error("Error: data and columns mismatch")
            invalid = True
            msg = "INVALID DATA"
            return None
        logger.info("Data ready.")
        return data, schema.columns


def pre_check(data, label_name):
    logger.info("Start to do pre check")
    global invalid
    global msg
    if label_name not in data.columns.tolist():
        invalid = True
        msg = "INVALID PARAMETER"
        logger.error("Error: %s not in data." % label_name)
        return
    try:
        data[label_name].astype(float)
    except:
        invalid = True
        msg = 'Invalid label type'
        logger.error('Error: label type must be int , float or double.')
        return
    try:
        data.drop([label_name], axis=1).astype(float)
    except:
        invalid = True
        msg = "invalid feature type"
        logger.error("Error: feature type must be int, float or double")
        return
    logger.info("Finish pre check")


def run_distributed(**param):
    global invalid
    global msg
    new_features = []

    arg_check(param)
    if invalid:
        return {"status": str(int(invalid)), "reaseon": msg, "features": new_features}
    logger.info("Start lr embeded feature selection.")
    input_path = param.get("inputPath")
    delimiter = param.get("delimiter")
    label_name = param.get("labelName")
    schema_path = param.get("schemaPath")
    lr_params = prepare_lr_params(param.get("param", {}))

    spark_session = SparkSession.builder.appName("featureSelectApplication").getOrCreate()
    data, cols = load_data(spark_session, input_path, schema_path, delimiter)
    if invalid:
        return {"status": str(int(invalid)), "reason": msg,
                "features": new_features}
    pre_check(pd.DataFrame(data.head(100), columns=cols), label_name)
    if invalid:
        return {"status": str(int(invalid)), "reason": msg, "features": new_features}
    num_partition = int(data.count() / num_per_partition) + 1
    if num_partition <= 2:
        try:
            res = data.rdd.coalesce(1, False).mapPartitions(lambda x: run(x, cols, lr_params, **param)).collect()
        except:
            invalid = True
            msg = "INVALID DATA"
            logger.error("Error: distributed training failed.")
            return {"status": str(int(invalid)), "reason": msg, "features": []}

        logger.info("Model initialization finished.")
        res.sort(key=lambda x: abs(x[1]), reverse=True)
        new_features = res
        logger.info("Finish feature selection.")
        logger.info("Done!")
        return {"status": str(int(invalid)), "reason": msg,
                "features": new_features}
    else:
        try:
            res = data.rdd.repartition(num_partition).mapPartitions(
                lambda x: run(x, cols, lr_params, **param)).collect()
        except:
            invalid = True
            msg = "INVALID DATA"
            logger.error("Error: distributed training falied.")
            return {"status": str(int(invalid)), "reason": msg, "features": []}
        logger.info("Model initialization finished.")
        res.sort(key=lambda x: x[0])
        res = [res[num_partition * i: num_partition * i + num_partition] for i in range(len(cols) - 1)]

        def process(x):
            n = len(x)
            feat = x[0][0]
            x = map(lambda x: x[1], x)
            x.sort()
            return (feat, sum(x[1:n - 1]) / 1.0 * (n - 2))

        new_features = map(process, res)
        new_features.sort(key=lambda x: abs(x[1]), reverse=True)
        logger.info("Finish feature selection")
        logger.info("Done!")
        return {"status": str(int(invalid)), "reason": msg,
                "features": new_features}


if __name__ == '__main__':
    if len(sys.argv) == 4:
        param = {
            'inputPath': sys.argv[1],
            'labelName': sys.argv[3],
            'param': {'appId': '0001', 'busiScene': 'score_name', 'name': 'model_name'},
            'delimiter': sys.argv[2]
        }
    elif len(sys.argv) == 5:
        param = {
            'inputPath': sys.argv[1],
            'schemaPath': sys.argv[4],
            'labelName': sys.argv[3],
            'param': {'appId': '0001', 'busiScene': 'score_name', 'name': 'model_name'},
            'delimiter': sys.argv[2]
        }
    res = run_distributed(**param)
    print(res)
