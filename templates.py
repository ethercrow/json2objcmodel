
HEADER_TEMPLATE = '''
@interface {name}: {parent_name}
{{
@private
{fields}
}}

{property_decls}

{method_decls}

@end

'''

FIELD_DECL_TEMPLATE = "    {objc_type} {name}_;"
PROPERTY_DECL_TEMPLATE = "@property({mem_policy}) {objc_type} {name};"
PROPERTY_SYNTH_TEMPLATE = "@synthesize {name} = {name}_;"

IMPLEMENTATION_TEMPLATE = '''
#import "{name}.h"

@implementation {name}

{property_synthesis}

{methods}

@end

'''

SETTER_DECLARATION = '- (void)setContent:(NSDictionary*)content;'

SETTER_BODY_TEMPLATE = '''- (void)setContent:(NSDictionary*)content
{{
{parse_lines}
}}
'''

FIELD_PARSE_LINE_TEMPLATE = '''
    self.{name} = [content objectForKey:@"{name}"];
    self.{name} = [[NSNull null] isEqual:self.{name}]?nil:self.{name};'''
INT_FIELD_PARSE_LINE_TEMPLATE = '''
    id boxed_{name} = [content objectForKey:@"{name}"];
    if (boxed_{name} && ![[NSNull null] isEqual:boxed_{name}])
        self.{name} = [boxed_{name} intValue];
    else
        self.{name} = 0;'''
DOUBLE_FIELD_PARSE_LINE_TEMPLATE = '''
    id boxed_{name} = [content objectForKey:@"{name}"];
    if (boxed_{name} && ![[NSNull null] isEqual:boxed_{name}])
        self.{name} = [boxed_{name} doubleValue];
    else
        self.{name} = 0.f;'''

DEALLOC_BODY_TEMPLATE = '''- (void)dealloc
{{
{release_lines}

    [super dealloc];
}}
'''

RELEASE_FIELD_LINE = '    [{name}_ release];'

