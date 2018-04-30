import sys

# include https://github.com/llvm-mirror/clang/tree/master/bindings/python in PYTHONPATH
from clang.cindex import CursorKind, Index

def process_function(node):
  params = [node.type.spelling + " " + node.spelling for node in node.get_children() if node.kind == CursorKind.PARM_DECL]
  print(node.type.spelling + " " + node.spelling + "(" + ", ".join(params) + ")")


def process_enum(node):
  #print(node.type.spelling + " " + node.spelling)
  pass


def process_hint(node):
  #print(node.type.spelling + " " + node.spelling)
  pass


def process_structs(node):
  #print(node.type.spelling + " " + node.spelling)
  pass


def walk(node):
  if node.spelling in func_syms and node.kind.is_declaration():
    func_syms[node.spelling].append(node.kind)
    process_function(node)
  elif node.spelling in enum_syms and node.is_definition():
    import ipdb; ipdb.set_trace()
    enum_syms[node.spelling].append(node.kind)
    process_enum(node)
  elif node.spelling in hint_syms and node.is_definition():
    hint_syms[node.spelling].append(node.kind)
    process_hint(node)
  elif node.spelling in struct_syms and node.is_definition():
    struct_syms[node.spelling].append(node.kind)
    process_structs(node)
  for n in node.get_children():
    walk(n)


if __name__ == '__main__':

  func_syms = {k: [] for k in open("symbols/functions.txt").read().split('\n')}
  enum_syms = {k: [] for k in open("symbols/enums.txt").read().split('\n')}
  hint_syms = {k: [] for k in open("symbols/hints.txt").read().split('\n')}
  struct_syms = {k: [] for k in open("symbols/structs.txt").read().split('\n')}
  syms = [func_syms, enum_syms, hint_syms, struct_syms]
  processors = [process_function, process_enum, process_hint, process_structs]

  index = Index.create()
  tu = index.parse(sys.argv[1])
  walk(tu.cursor)
