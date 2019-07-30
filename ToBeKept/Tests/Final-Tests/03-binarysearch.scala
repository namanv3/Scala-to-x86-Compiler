object binarysearch {
	def bsearch(arr: Array[Int], key : Int) : Int = {
		var start = 0
		var end = arr.length - 1

		while (start <= end) {
			val mid = start + (end - start) / 2
			println(start, mid, end)
			if (arr(mid) == key) return mid
			if (arr(mid) > key) end = mid - 1
			else start = mid + 1
		}
		return -1
	}

	def main(args: Array[String]) {
		val arr = Array(12, 23, 99, 111, 199, 212, 1000)
		println(bsearch(arr,99))
	}
}