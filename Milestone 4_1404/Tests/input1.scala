object find_cube {
		def func(x : Array[Int]) : Int = {
				val arr = Array(1,2,3,4)

				// var ss = x match {
				//   case 9 => 1
				//   case 7 => 2
				//   case 2 => 3
				//   case _ => 4
				// }
				x match {
				  case 9 => func(5)
				  case 7 => var x = 3
				  case 2 => val y = 1
				  case _ => func(1)
				}
		}
}
