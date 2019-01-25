object find_cube {
	def main(args: Array[String]) = {
		val cube = (x: Int) => x * x * x

		val n: Int = 9
		println(cube(n))
	}
}