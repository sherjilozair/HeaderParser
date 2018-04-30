import sys

# include https://github.com/llvm-mirror/clang/tree/master/bindings/python in PYTHONPATH
from clang.cindex import CursorKind, Index

def process_structs(node):
  return []


def process_function(node):
  params = [node.type.spelling + " " + node.spelling for node in node.get_children() if node.kind == CursorKind.PARM_DECL]
  return [node.type.spelling + " " + node.spelling + "(" + ", ".join(params) + ")"]


def process_enum(node):
  return []  # TODO


def process_typedef(node):
  return [] # TODO


def process_union(node):
  return []  # TODO


def walk_SDL(node):
  if node.kind == CursorKind.STRUCT_DECL:
    return process_structs(node)
  if node.kind == CursorKind.FUNCTION_DECL:
    return process_function(node)
  if node.kind == CursorKind.ENUM_CONSTANT_DECL:
    return process_enum(node)
  if node.kind == CursorKind.TYPEDEF_DECL:
    return process_typedef(node)
  if node.kind == CursorKind.UNION_DECL:
    return process_union(node)
  else:
    return []

def walk(node):
  if node.spelling.startswith("SDL_"):
    return walk_SDL(node)
  else:
    return sum([walk(child) for child in node.get_children()], [])
      

index = Index.create()
tu = index.parse(sys.argv[1])
li = walk(tu.cursor)
for n in li:
  print(n)
