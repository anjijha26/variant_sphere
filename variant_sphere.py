from pxr import Usd, UsdGeom, UsdShade, Sdf

stage = Usd.Stage.CreateNew("variant_sphere.usda")


sphere = UsdGeom.Sphere.Define(stage, "/World/Sphere")

material_scope = UsdGeom.Scope.Define(stage, "/World/Materials")

def create_material(name, color):
    mat = UsdShade.Material.Define(stage, "/World/Materials/{}".format(name))
    shader = UsdShade.Shader.Define(stage, "/World/Materials/{}/Shader".format(name))
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(color)
    mat.CreateSurfaceOutput().ConnectToSource(shader, "surface")
    return mat

red = create_material("Red", (1, 0, 0))
green = create_material("Green", (0, 1, 0))
blue = create_material("Blue", (0, 0, 1))

variants = sphere.GetPrim().GetVariantSets().AddVariantSet("look")
for name, mat in [("Red", red), ("Green", green), ("Blue", blue)]:
    variants.AddVariant(name)
    variants.SetVariantSelection(name)
    with variants.GetVariantEditContext():
        UsdShade.MaterialBindingAPI(sphere).Bind(mat)

stage.GetRootLayer().Save()
print("USD file created: variant_sphere.usda")
