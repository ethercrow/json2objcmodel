from templates import *

TYPE_TYPE_MAP = {
       list:"NSMutableArray*",
       dict:"NSMutableDictionary*",
        str:"NSString*",
        int:"int",
       bool:"bool",
      float:"double"
}

class ObjCClass():

    class ObjCClassField():
        def __init__(self, name, objc_type):
            self.name = name
            self.objc_type = objc_type

        def __str__(self):
            return "{} {};".format(self.objc_type, self.name)

    def __init__(self, name):

        self.parent_name = "NSObject"
        self.name = name
        self.fields = []
        self.methods = [] # declaration:definition pairs

    def add_field(self, name, T):

        self.fields.append(self.ObjCClassField(name, T))

    def __repr__(self):

        result = "<ObjCClass " + self.name + " with fields:\n"
        result += "\n".join(map(str, self.fields))
        result += "\n>\n"
        return result

    def dump_header(self):

        def declare_field(f):
            return FIELD_DECL_TEMPLATE.format(objc_type=f.objc_type, name=f.name)

        def declare_property(f):
            mem_policy = 'retain'
            if f.objc_type in ['int', 'double', 'bool']:
                mem_policy = 'assign'

            return PROPERTY_DECL_TEMPLATE.format(objc_type=f.objc_type,
                    name=f.name, mem_policy=mem_policy)

        fields = "\n".join(map(declare_field, self.fields))
        property_decls = "\n".join(map(declare_property, self.fields))

        result = HEADER_TEMPLATE.format(name=self.name, parent_name=self.parent_name,
                fields=fields, property_decls=property_decls,
                method_decls=SETTER_DECLARATION)

        return result

    def dump_implementation(self):

        def synthesize_property(f):
            return PROPERTY_SYNTH_TEMPLATE.format(name=f.name)

        property_synthesis = "\n".join(map(synthesize_property, self.fields))

        def release_field(f):
            return RELEASE_FIELD_LINE.format(name=f.name)

        ptr_fields = [f for f in self.fields if f.objc_type[-1] == '*']
        release_lines = "\n".join(map(release_field, ptr_fields))
        dealloc_body = DEALLOC_BODY_TEMPLATE.format(release_lines=release_lines)

        def parse_field(f):
            template = FIELD_PARSE_LINE_TEMPLATE
            if f.objc_type == "int":
                template = INT_FIELD_PARSE_LINE_TEMPLATE
            elif f.objc_type == "double":
                template = DOUBLE_FIELD_PARSE_LINE_TEMPLATE
            elif f.objc_type == "bool":
                template = BOOL_FIELD_PARSE_LINE_TEMPLATE
            return template.format(name=f.name)

        parse_lines = "\n".join(map(parse_field, self.fields))
        setter_body = SETTER_BODY_TEMPLATE.format(parse_lines=parse_lines)

        methods = setter_body + '\n' + dealloc_body

        result = IMPLEMENTATION_TEMPLATE.format(name=self.name,
                methods=methods, property_synthesis=property_synthesis)
        return result;
