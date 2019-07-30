object test3 {
	def println() = {

	}
	def main(args : Array[String]) = {
		var arr : Int = 12

		while (arr > 0) {
			println(arr)
			var decr : Int = 3
			arr -= decr
		}
	}
}
