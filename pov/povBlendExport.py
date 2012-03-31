import bpy
import os

class HelloWorldPanel(bpy.types.Panel):
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Hello world!", icon='WORLD_DATA')

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(obj, "name")


def register():
    bpy.utils.register_class(HelloWorldPanel)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)


def get_used_materials():
    """ Collect Materials used in the selected object. 
    """
    m_list = []
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            for f in obj.data.faces:
                if f.material_index < len(bpy.data.materials):
                    m_list.append(f.material_index)
    return set(m_list)


def get_used_textures():
    """ Collect images from the UV images and Material texture slots 
    """
    tex_list = {}
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            if EXPORT_UV_IMAGE_AS_TEXTURE:
                for num, uv in enumerate(obj.data.uv_textures):
                    for f in uv.data:
                        if f.use_image:
                            if f.image.source == 'FILE':
                                if not f.image.name in tex_list:
                                    name = uv.name
                                    if num == 0: name = ''
                                    t_path = bpy.path.abspath(f.image.filepath)
                                    if COPY_TEX_FILES:
                                        t_path = save_image(f.image)
                                    tex_list[f.image.name] = (name, t_path, 'MODULATE')

            for f in obj.data.faces:
                if f.material_index < len(bpy.data.materials):
                    for tex in bpy.data.materials[f.material_index].texture_slots:
                        if ((tex) and (not tex.texture.use_nodes)):
                            if tex.texture_coords == 'UV' and obj.data.uv_textures:
                                if tex.uv_layer:
                                    uv_name = tex.uv_layer
                                    if not [uv.name for uv in obj.data.uv_textures].index(uv_name):
                                        uv_name = ''
                                else:
                                    uv_name = '' #obj.data.uv_textures[0].name
                                if tex.texture.image.source == 'FILE':
                                    if not tex.texture.name in list(tex_list.keys()):
                                        #try:
                                            envtype = 'MODULATE'
                                            if tex.use_map_normal:
                                                envtype = 'NORMAL'
                                            t_path = bpy.path.abspath(tex.texture.image.filepath)
                                            if COPY_TEX_FILES:
                                                t_path = save_image(tex.texture.image)
                                            tex_list[tex.texture.name] = (uv_name, t_path, envtype)
                                        #except:
                                        #    print('ERROR: can\'t get texture image on %s.' % tex.texture.name)
    return tex_list

if __name__ == "__main__":
    register()
    
    active_object = bpy.context.active_object # active object on scene
    data = active_object.data

    s = ""
    s += "mesh {\n"
    s += "inside_vector <0, 1, 0>\n"
    vertices = []
    normals = []
    
    #for vertex in bpy.data.objects["Cube"].data.vertices:
    for vertex in data.vertices:
        x = vertex.co.x
        y = vertex.co.y
        z = vertex.co.z
        nx = vertex.normal.x
        ny = vertex.normal.y
        nz = vertex.normal.z
        vertices.append("<%s, %s, %s>" % (x, z, y))
        normals.append("<%s, %s, %s>" % (nx, nz, ny))
    
    c = 1    
    faces = data.faces[:]
    for face in faces:
        fi = face.vertices[:]
        if len(fi) == 3:
            s += "smooth_triangle {\n"
            s += "\t" + vertices[fi[0]] + ", " + normals[fi[0]] + ",\n"
            s += "\t" + vertices[fi[1]] + ", " + normals[fi[1]] + ",\n"
            s += "\t" + vertices[fi[2]] + ", " + normals[fi[2]] + "\n"
            if c == 1:
                s += "texture { pigment{Red}  } }\n\n"
                c = 2
            else:
                s += "texture { pigment{Blue}  } }\n\n"
                c = 1



            
        elif len(fi) == 4:
            s += "smooth_triangle {\n"
            s += "\t" + vertices[fi[0]] + ", " + normals[fi[0]] + ",\n"
            s += "\t" + vertices[fi[1]] + ", " + normals[fi[1]] + ",\n"
            s += "\t" + vertices[fi[2]] + ", " + normals[fi[2]] + "\n"
            if c == 1:
                s += "texture { T_Stone12 } }\n\n"
                c = 2
            else:
                s += "texture { T_Stone10 } }\n\n"
                c = 1
            s += "smooth_triangle {\n"
            s += "\t" + vertices[fi[3]] + ", " + normals[fi[3]] + ",\n"
            s += "\t" + vertices[fi[2]] + ", " + normals[fi[2]] + ",\n"
            s += "\t" + vertices[fi[0]] + ", " + normals[fi[0]] + "\n"
            if c == 1:
                s += "texture {T_Stone12} }\n\n"
                c = 2
            else:
                s += "texture {T_Stone10} }\n\n"
                c = 1
    
    s += "}\n"
    s += "// materials used : \n"
    for m_idx in get_used_materials():
        mat = bpy.data.materials[m_idx]
        r, g, b = mat.diffuse_color[0], mat.diffuse_color[1], mat.diffuse_color[2]
        s+= "//%s : <%s, %s, %s>\n" % (m_idx, r, g, b)
    filepath = "/home/arikel/programmation/pygame/projects/dm/pov/aritest.txt"
    dest_dir = os.path.dirname(filepath)
    f = open(filepath, "w")
    f.write(s)
    f.close()
    
