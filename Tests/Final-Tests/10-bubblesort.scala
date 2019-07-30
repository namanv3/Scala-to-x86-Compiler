object bubblesort {
	def bsort (arr : Array[Int]) {
		val n = arr.length
		for (i <- 0 to (n - 2)) {
			for (j <- 0 to (n - i - 2)) {
				if (arr(j) > arr(j+1)) {
					val temp = arr(j)
					arr(j) = arr(j+1)
					arr(j+1) = temp
				}
			}
		}
	}

	def main(args : Array[String]) {
		val n = scala.io.StdIn.readInt()
		var arr = new Array[Int](n)

		for (i <- 0 to n - 1) {
			arr(i) = scala.io.StdIn.readInt()
		}

		bsort(arr)
		for (i <- arr) println(i)
	}
}