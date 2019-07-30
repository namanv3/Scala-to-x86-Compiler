object quicksort {
	def partition(arr : Array[Int], pivot : Int, start : Int, end : Int) : Int = {
		var j = start + 1
		var i = end
		while (i > j) {
			while (arr(i) < pivot) {
				val temp = arr(i)
				arr(i) = arr(j)
				arr(j) = temp
				j += 1
			}
			i -= 1
		}
		val temp = arr(j)
		arr(j) = arr(start)
		arr(start) = temp

		return j
	}

	def qsort (arr : Array[Int], start : Int, end : Int) {
		if (start >= end) return

		val pivot = arr(start)
		val p_index = partition(arr, pivot, start, end)
		for (i <- arr) println(i)
		println("")

		qsort(arr, start, p_index - 1)
		qsort(arr, p_index + 1, end)
	}

	def main (args: Array[String]) {
		val arr = Array(11,22,3,44,4,99,30,0)
		for (i <- arr) println(i)
		println("")
		qsort(arr, 0 , arr.length - 1)
		for (i <- arr) println(i)
		println("")
	}
}
