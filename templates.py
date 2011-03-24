
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

FIELD_PARSE_LINE_TEMPLATE = '    self.{name} = [content objectForKey:"{name}"];'
INT_FIELD_PARSE_LINE_TEMPLATE = '    self.{name} = [[content objectForKey:"{name}"] intValue];'

DEALLOC_BODY_TEMPLATE = '''- (void)dealloc
{{
{release_lines}

    [super dealloc];
}}
'''

RELEASE_FIELD_LINE = '    [{name}_ release];'

