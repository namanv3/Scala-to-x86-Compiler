object min_element {
	def main(args: Array[String]) = {
		println("Time to find the shortest element in an array")

		val arr = Array(103,222,33,49,95,31)
		println(s"First element: ${arr(0)}")

		val min_element = ( x : Array[Int]) => {
			var min_val = x(0)
			for (num <- x) {
				if (num < min_val) {
					min_val = num
				}
			}
			min_val
		}

		println(s"Min element: ${min_element(arr)}")
	}
}