import sys

# include https://github.com/llvm-mirror/clang/tree/master/bindings/python in PYTHONPATH
from clang.cindex import CursorKind, Index

def process_function(node):
  params = [node.type.spelling + " " + node.spelling for node in node.get_children() if node.kind == CursorKind.PARM_DECL]
  print(node.type.spelling + " " + node.spelling + "(" + ", ".join(params) + ")")


def process_enum(node):
  pass


def process_hint(node):
  pass


def process_structs(node):
  pass


def walk(node):
  for i in range(4):
    if node.spelling in syms[i]:
      processors[i](node)
  for n in node.get_children():
    walk(n)


if __name__ == '__main__':

  func_syms = set(open("symbols/functions.txt").read().split('\n'))
  enum_syms = set(open("symbols/enums.txt").read().split('\n'))
  hint_syms = set(open("symbols/hints.txt").read().split('\n'))
  struct_syms = set(open("symbols/structs.txt").read().split('\n'))
  syms = [func_syms, enum_syms, hint_syms, struct_syms]
  processors = [process_function, process_enum, process_hint, process_structs]

  index = Index.create()
  tu = index.parse(sys.argv[1])
  walk(tu.cursor)
