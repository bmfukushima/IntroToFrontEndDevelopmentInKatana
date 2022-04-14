
parent_node = NodegraphAPI.GetRootNode()


############################################
############## SETUP GEOMETRY ##############
############################################
primitive_create_node = NodegraphAPI.CreateNode("PrimitiveCreate", parent_node)


############################################
############### SETUP LIGHTS ###############
############################################
gaffer_three_node = NodegraphAPI.CreateNode("GafferThree", parent_node)
""" Here we will create a new light in the Gaffer Three that we've created above,
and then we will set the color of that light to be red"""
# Create new light
root_package = gaffer_three_node.getRootPackage()
light_package = root_package.createChildPackage("AreaLightPackage", "newLight")

# position light
light_package.getCreateNode().getParameter("transform.translate.z").setValue(3, 0)

# Get light material
light_mat_node = light_package.getMaterialNode()
light_mat_node.checkDynamicParameters()

# Set color
light_mat_node.getParameter('shaders.dlLightParams.color.enable').setValue(1, 1)
light_mat_node.getParameter('shaders.dlLightParams.color.value.i1').setValue(0, 1)
light_mat_node.getParameter('shaders.dlLightParams.color.value.i2').setValue(0, 1)


############################################
############### SETUP CAMERA ###############
############################################
""" We will translate the camera in the Z axis so that our sphere will be framed """
camera_create_node = NodegraphAPI.CreateNode("CameraCreate", parent_node)
camera_create_node.getParameter('transform.translate.z').setValue(3, 0)


############################################
############## SETUP MATERIAL ##############
############################################
# Create material
material_node = NodegraphAPI.CreateNode("Material", parent_node)
material_node.setShader("dlSurface", "dlPrincipled")

# Assign material
material_assign_node = NodegraphAPI.CreateNode("MaterialAssign", parent_node)
material_assign_node.getParameter('CEL').setValue(primitive_create_node.getScenegraphLocation(), 0)
material_assign_node.getParameter('args.materialAssign.value').setValue(material_node.getScenegraphLocation(), 0)


############################################
############### CONNECT NODES ##############
############################################
merge_node = NodegraphAPI.CreateNode("Merge", parent_node)

# Create ports on merge node and connect
""" Here we will setup the ports and connections to wire our graph together """
geo_in_port = merge_node.addInputPort("in_geo")
cam_in_port = merge_node.addInputPort("in_cam")

# connect ports
geo_in_port.connect(primitive_create_node.getOutputPortByIndex(0))
cam_in_port.connect(camera_create_node.getOutputPortByIndex(0))
merge_node.getOutputPortByIndex(0).connect(gaffer_three_node.getInputPortByIndex(0))
gaffer_three_node.getOutputPortByIndex(0).connect(material_node.getInputPortByIndex(0))
material_node.getOutputPortByIndex(0).connect(material_assign_node.getInputPortByIndex(0))


############################################
############### POSITION NODES #############
############################################
""" Here we will position all of our nodes so that they don't get auto laid out
on top of themselves """
NodegraphAPI.SetNodePosition(primitive_create_node, (-100, 0))
NodegraphAPI.SetNodePosition(camera_create_node, (100, 0))
NodegraphAPI.SetNodePosition(merge_node, (0, -100))
NodegraphAPI.SetNodePosition(gaffer_three_node, (0, -200))
NodegraphAPI.SetNodePosition(material_node, (0, -300))
NodegraphAPI.SetNodePosition(material_assign_node, (0, -400))