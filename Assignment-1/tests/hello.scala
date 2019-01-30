object hello {
	def main(args: Array[String]) = {
		println("Time to find the first element in an array")	// do comments even wooooork

		/*
		object hello {
	def main(args: Array[String]) = {
		println("Time to find the first element in an array")	// do comments even wooooork

		val arr = Array(13,222,33,49,95,31)
		println(s"First element: ${arr(0)}")
	}
}
		*/

		val arr_myprecious = Array(13,222,33,49,95,31)
		println(s"First element: ${arr(0)}")
		val _arr_myprecious = Array(13,222,33,49,95,31)
		println(s"First element: ${arr(0)}")

		val x: Int = 12

		x match {
		  case 0 => "zero"
		  case 1 => "one"
		  case 2 => "two"
		  case _ => "many"
		}
	}
}