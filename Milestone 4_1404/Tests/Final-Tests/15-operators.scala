object operators {
	def main(args : Array[String]) {
		val a = scala.io.StdIn.readFloat()
		val b = scala.io.StdIn.readInt()
		var c = a - 9.0 + (8 * b)
		println(a,b,c)
	}
}