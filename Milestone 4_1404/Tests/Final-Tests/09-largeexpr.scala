object largeExpr {
	def f (a : Int, b : Int, c : Int, d : Int, e : Int, f : Int, g : Int, h : Int) : Int = {
		return a + b * c / d % e ^ f | g & h 
	}

	def main(args : Array[String]) {
		println(f(1,2,3,5,8,13,21,34))
	}
}