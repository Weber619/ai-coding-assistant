import ast
from typing import Dict, Any

async def optimize_code(code: str) -> Dict[str, Any]:
    try:
        tree = ast.parse(code)
        optimizer = CodeOptimizer()
        optimized_tree = optimizer.visit(tree)
        optimized_code = ast.unparse(optimized_tree)
        
        return {
            "original_code": code,
            "optimized_code": optimized_code,
            "optimizations": optimizer.optimizations
        }
    except Exception as e:
        raise Exception(f"Error optimizing code: {str(e)}")

class CodeOptimizer(ast.NodeTransformer):
    def __init__(self):
        self.optimizations = []

    def visit_For(self, node):
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
            if len(node.iter.args) == 1 and isinstance(node.iter.args[0], ast.Constant) and isinstance(node.iter.args[0].value, (int, float)):
                self.optimizations.append("Replaced range() with list comprehension")
                return ast.Expr(ast.ListComp(
                    elt=ast.Call(func=ast.Name(id='print', ctx=ast.Load()), args=[ast.Name(id=node.target.id, ctx=ast.Load())], keywords=[]),
                    generators=[
                        ast.comprehension(
                            target=node.target,
                            iter=node.iter,
                            ifs=[],
                            is_async=0
                        )
                    ]
                ))
        return node

    def visit_If(self, node):
        if isinstance(node.test, ast.Compare) and len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.Eq):
            if isinstance(node.test.left, ast.Name) and isinstance(node.test.comparators[0], ast.Constant) and isinstance(node.test.comparators[0].value, str):
                self.optimizations.append("Replaced if x == 'string' with if x is 'string'")
                node.test.ops = [ast.Is()]
        return node

    def visit_BinOp(self, node):
        if isinstance(node.op, ast.Add) and isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
            if isinstance(node.left.value, str) and isinstance(node.right.value, str):
                self.optimizations.append("Combined string literals")
                return ast.Constant(value=node.left.value + node.right.value)
        return node

    def visit_ListComp(self, node):
        if isinstance(node.elt, ast.Call) and isinstance(node.elt.func, ast.Name) and node.elt.func.id == 'len':
            if len(node.generators) == 1 and not node.generators[0].ifs:
                self.optimizations.append("Replaced list comprehension with map(len, ...)")
                return ast.Call(
                    func=ast.Name(id='map', ctx=ast.Load()),
                    args=[
                        ast.Name(id='len', ctx=ast.Load()),
                        node.generators[0].iter
                    ],
                    keywords=[]
                )
        return node

    def visit_Compare(self, node):
        if isinstance(node.ops[0], ast.In) and isinstance(node.comparators[0], ast.List):
            self.optimizations.append("Replaced list with set for membership testing")
            node.comparators[0] = ast.Set(elts=node.comparators[0].elts)
        return node

    def visit_FunctionDef(self, node):
        for i, stmt in enumerate(node.body):
            if isinstance(stmt, ast.Return) and i > 0:
                prev_stmt = node.body[i-1]
                if isinstance(prev_stmt, ast.If) and not prev_stmt.orelse:
                    self.optimizations.append("Simplified if-return pattern")
                    node.body[i-1] = ast.Return(value=prev_stmt.test)
                    node.body.pop(i)
        return node

async def main():
    code = input("Enter the Python code to optimize:\n")
    
    try:
        optimization_result = await optimize_code(code)
        print("\nOriginal Code:")
        print(optimization_result['original_code'])
        print("\nOptimized Code:")
        print(optimization_result['optimized_code'])
        print("\nOptimizations applied:")
        for opt in optimization_result['optimizations']:
            print(f"- {opt}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())