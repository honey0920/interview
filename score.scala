import org.apache.spark.rdd.RDD
import breeze.linalg.{DenseMatrix => BDM}
import org.apache.spark.mllib.linalg.{Matrices, Matrix, Vector, Vectors}
import scala.collection.mutable
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.stat.{MultivariateStatisticalSummary, Statistics}

private[spark] class FeatureScore {
  def VarFeatures(data: RDD[LabeledPoint]): Array[FeatureCriterion] = {
    val numCols = data.first().features.size
    val results = new Array[Double](numCols)
    val allfeatures = data.map{
      case LabeledPoint(label, features) =>
        features
    }
    val summary: MultivariateStatisticalSummary = Statistics.colStats(allfeatures)
    summary.variance.toArray.zipWithIndex.map(p => {
      val variance = new FeatureCriterion().init(p._2, p._1)
      variance
    })
  }
// accelerate cov computation using aggregate
  def CovFeatures(data: RDD[LabeledPoint]): Array[FeatureCriterion] = {
    val numCols = data.first().features.size
    val results = data.treeAggregate(Array.fill[CovarianceCounter](numCols)(new CovarianceCounter()))(
      seqOp = (counterArr, row) => counterArr.zip(row.features.toArray).map(x => x._1.add(row.label, x._2)),
      combOp = (baseCounterArr, other) => baseCounterArr.zip(other).map(x => x._1.merge(x._2))
    ).map(counts => counts.Ck / math.sqrt(counts.MkX * counts.MkY))
    results.zipWithIndex.map(p => {
      val cch = new FeatureCriterion().init(p._2, p._1)
      cch
    })
  }
  def chiSquaredFeatures(data: RDD[LabeledPoint]): Array[FeatureCriterion] = {
    val numCols = data.first().features.size
    val results = new Array[Double](numCols)
    var labels: Map[Double, Int] = null
    // at most 1000 columns at a time
    val batchSize = 1000
    var batch = 0
    while (batch * batchSize < numCols) {
      // The following block of code can be cleaned up and made public as
      // chiSquared(data: RDD[(V1, V2)])
      val startCol = batch * batchSize
      val endCol = startCol + math.min(batchSize, numCols - startCol)
      val pairCounts = data.mapPartitions { iter =>
        val distinctLabels = mutable.HashSet.empty[Double]
        val allDistinctFeatures: Map[Int, mutable.HashSet[Double]] =
          Map((startCol until endCol).map(col => (col, mutable.HashSet.empty[Double])): _*)
        iter.flatMap { case LabeledPoint(label, features) =>
          distinctLabels += label
          val brzFeatures = features.asBreeze
          (startCol until endCol).map { col =>
            val feature = brzFeatures(col)
            allDistinctFeatures(col) += feature
            (col, feature, label)
          }
        }
      }.countByValue()
      if (labels == null) {
        // Do this only once for the first column since labels are invariant across features.
        labels =
          pairCounts.keys.filter(_._1 == startCol).map(_._3).toArray.distinct.zipWithIndex.toMap
      }
      val numLabels = labels.size
      pairCounts.keys.groupBy(_._1).foreach { case (col, keys) =>
        val features = keys.map(_._2).toArray.distinct.zipWithIndex.toMap
        val numRows = features.size
        val contingency = new BDM(numRows, numLabels, new Array[Double](numRows * numLabels))
        keys.foreach { case (_, feature, label) =>
          val i = features(feature)
          val j = labels(label)
          contingency(i, j) += pairCounts((col, feature, label))
        }
        results(col) = chiSquaredMatrix(Matrices.fromBreeze(contingency))
      }
      batch += 1
    }
    results.zipWithIndex.map(p => {
      val chi = new FeatureCriterion().init(p._2, p._1)
      chi
    })
  }
  def MutualInfoFeatures(data: RDD[LabeledPoint]): Array[FeatureCriterion] = {
    val numCols = data.first().features.size
    val results = new Array[Double](numCols)
    var labels: Map[Double, Int] = null
    // at most 1000 columns at a time
    val batchSize = 1000
    var batch = 0
    while (batch * batchSize < numCols) {
      // The following block of code can be cleaned up and made public as
      // chiSquared(data: RDD[(V1, V2)])
      val startCol = batch * batchSize
      val endCol = startCol + math.min(batchSize, numCols - startCol)
      val pairCounts = data.mapPartitions { iter =>
        val distinctLabels = mutable.HashSet.empty[Double]
        val allDistinctFeatures: Map[Int, mutable.HashSet[Double]] =
          Map((startCol until endCol).map(col => (col, mutable.HashSet.empty[Double])): _*)
        iter.flatMap { case LabeledPoint(label, features) =>
          distinctLabels += label
          val brzFeatures = features.asBreeze
          (startCol until endCol).map { col =>
            val feature = brzFeatures(col)
            allDistinctFeatures(col) += feature
            (col, feature, label)
          }
        }
      }.countByValue()
      if (labels == null) {
        // Do this only once for the first column since labels are invariant across features.
        labels =
          pairCounts.keys.filter(_._1 == startCol).map(_._3).toArray.distinct.zipWithIndex.toMap
      }
      val numLabels = labels.size
      pairCounts.keys.groupBy(_._1).foreach { case (col, keys) =>
        val features = keys.map(_._2).toArray.distinct.zipWithIndex.toMap
        val numRows = features.size
        val contingency = new BDM(numRows, numLabels, new Array[Double](numRows * numLabels))
        keys.foreach { case (_, feature, label) =>
          val i = features(feature)
          val j = labels(label)
          contingency(i, j) += pairCounts((col, feature, label))
        }
        results(col) = MutualInfoMatrix(Matrices.fromBreeze(contingency))
      }
      batch += 1
    }
    results.zipWithIndex.map(p => {
      val mim = new FeatureCriterion().init(p._2, p._1)
      mim
    })
  }
  /*
   * Pearson's independence test on the input contingency matrix.
   * TODO: optimize for SparseMatrix when it becomes supported.
   */
  def chiSquaredMatrix(counts: Matrix): Double = {
    val numRows = counts.numRows
    val numCols = counts.numCols
    // get row and column sums
    val colSums = new Array[Double](numCols)
    val rowSums = new Array[Double](numRows)
    val colMajorArr = counts.toArray
    val colMajorArrLen = colMajorArr.length
    var i = 0
    while (i < colMajorArrLen) {
      val elem = colMajorArr(i)
      colSums(i / numRows) += elem
      rowSums(i % numRows) += elem
      i += 1
    }
    val total = colSums.sum
    // second pass to collect statistic
    var statistic = 0.0
    var j = 0
    while (j < colMajorArrLen) {
      val col = j / numRows
      val colSum = colSums(col)
      val row = j % numRows
      val rowSum = rowSums(row)
      val expected = colSum * rowSum / total
      statistic += (colMajorArr(j) - expected) * (colMajorArr(j) - expected) / expected
      j += 1
    }
    statistic
  }
  def MutualInfoMatrix(counts: Matrix): Double = {
    val numRows = counts.numRows
    val numCols = counts.numCols
    // get row and column sums
    val colSums = new Array[Double](numCols)
    val rowSums = new Array[Double](numRows)
    val colMajorArr = counts.toArray
    val colMajorArrLen = colMajorArr.length
  //  println("colMajorArr: " + colMajorArr.mkString(" "))
    var i = 0
    while(i < colMajorArrLen){
      val elem = colMajorArr(i)
      colSums(i / numRows) += elem
      rowSums(i % numRows) += elem
      i += 1
  }
    val total = colSums.sum
    var statistic = 0.0
    var j = 0
    while (j < colMajorArrLen) {
      val col = j / numRows
      val colSum = colSums(col)
      val row = j % numRows
      val rowSum = rowSums(row)
      val px = rowSums(row) / total
      val py = colSums(col) / total
      val pxy = colMajorArr(j) /total
     // println("prob: " + pxy/ (px * py))
      if( pxy != 0)
        statistic += pxy * (math.log(pxy/ (px * py)) / math.log(2))
      j += 1
    }
    statistic
  }
}
private class CovarianceCounter extends Serializable {
  var xAvg = 0.0 // the mean of all examples seen so far in col1
  var yAvg = 0.0 // the mean of all examples seen so far in col2
  var Ck = 0.0 // the co-moment after k examples
  var MkX = 0.0 // sum of squares of differences from the (current) mean for col1
  var MkY = 0.0 // sum of squares of differences from the (current) mean for col2
  var count = 0L // count of observed examples
  // add an example to the calculation
  def add(x: Double, y: Double): this.type = {
    val deltaX = x - xAvg
    val deltaY = y - yAvg
    count += 1
    xAvg += deltaX / count
    yAvg += deltaY / count
    Ck += deltaX * (y - yAvg)
    MkX += deltaX * (x - xAvg)
    MkY += deltaY * (y - yAvg)
    this
  }
  // merge counters from other partitions. Formula can be found at:
  // http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
  def merge(other: CovarianceCounter): this.type = {
    if (other.count > 0) {
      val totalCount = count + other.count
      val deltaX = xAvg - other.xAvg
      val deltaY = yAvg - other.yAvg
      Ck += other.Ck + deltaX * deltaY * count / totalCount * other.count
      xAvg = (xAvg * count + other.xAvg * other.count) / totalCount
      yAvg = (yAvg * count + other.yAvg * other.count) / totalCount
      MkX += other.MkX + deltaX * deltaX * count / totalCount * other.count
      MkY += other.MkY + deltaY * deltaY * count / totalCount * other.count
      count = totalCount
    }
    this
  }
  // return the sample covariance for the observed examples
  def cov: Double = Ck / (count - 1)
}