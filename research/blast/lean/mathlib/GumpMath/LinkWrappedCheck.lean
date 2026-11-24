/-
`TorusNb` checked by the kernel (`decide +kernel`) on more wrapped faces, hence `wrapped_full` there.
-/
import GumpMath.LinkWrappedFull

namespace Gump.Link.Wrapped

theorem torusNb_1_0_2 : TorusNb 1 0 2 := torusNb_of (by decide +kernel)
theorem torusNb_2_0_1 : TorusNb 2 0 1 := torusNb_of (by decide +kernel)
theorem torusNb_1_0_3 : TorusNb 1 0 3 := torusNb_of (by decide +kernel)
theorem torusNb_3_0_1 : TorusNb 3 0 1 := torusNb_of (by decide +kernel)
theorem torusNb_2_1_2 : TorusNb 2 1 2 := torusNb_of (by decide +kernel)
theorem torusNb_2_0_3 : TorusNb 2 0 3 := torusNb_of (by decide +kernel)
theorem torusNb_3_1_3 : TorusNb 3 1 3 := torusNb_of (by decide +kernel)
theorem torusNb_3_0_3 : TorusNb 3 0 3 := torusNb_of (by decide +kernel)

end Gump.Link.Wrapped
