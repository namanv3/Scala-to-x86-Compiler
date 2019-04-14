object shortcircuit {
	def main(args : Array[String]) {
		val a = scala.io.StdIn.readInt()
		if (2 < 3 || 2/a == 3) {
			println("shorted")
		}
	}
}