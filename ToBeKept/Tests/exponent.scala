object recurse {
	def exponentiation (a : Int, b : Int) : Int  = {
		if (a == 0) {
			return 1
		}
		if (b == 0) {
			return 1
		}

		var y : Int = a
		if (b % 2 == 0) {
			y = exponentiation(a, b/2);
			y = y * y
		}
		else {
			y = (y * exponentiation(a, b - 1))
		}
		return y
	}

	def main () = {
		exponentiation(12, 3)
	}
}
