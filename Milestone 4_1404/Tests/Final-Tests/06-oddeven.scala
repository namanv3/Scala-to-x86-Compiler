object oddeven {
	// def odd (n : Int) : Boolean
	def even (n : Int) : Boolean = {
		if (n == 0) return true
		return odd(n - 1)
	}

	def odd (n : Int) : Boolean = {
		if (n == 0) return false
		return even(n - 1)
	}

	def main(args : Array[String]) {
		if (even(8)) {
			println("its even")
		}
	}
}