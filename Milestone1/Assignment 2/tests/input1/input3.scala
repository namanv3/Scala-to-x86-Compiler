object min_element_m {
	def min_element (x : Array[Int]) : Int = {
		var min_val = x(0)
		for (num <- x) {
			if (num < min_val) {
				min_val = num
			}
		}
		return min_val
	}
	def main(args: Array[String]) = {
		println("Time to find the shortest element in an array")
		val arr = Array(103,222,33,49,95,31)
		println(s"First element: ${arr(0)}")
		println(s"Min element: ${min_element(arr)}")
	}
}
