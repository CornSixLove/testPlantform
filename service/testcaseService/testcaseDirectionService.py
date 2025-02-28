# creator: LiFree
# 编写时间： 2025/2/5 10:20
from sqlalchemy import exists
from sqlalchemy.orm import Session

from models.dao.TestcaseDirectoryDao import TestcaseDirectory


def search_directories_tree(db: Session, name: str):
    # 1. 查询所有名称包含关键字的叶子节点（没有子节点的节点）
    leaves_query = db.query(TestcaseDirectory).filter(
        TestcaseDirectory.testDirectory_name.like(f"%{name}%"),
        ~exists().where(TestcaseDirectory.pid == TestcaseDirectory.id)  # 没有子节点的才是叶子
    )
    leaf_nodes = leaves_query.all()

    # 2. 收集所有相关节点（叶子节点 + 所有祖先节点）
    node_ids = set()
    for leaf in leaf_nodes:
        current = leaf
        while current:
            node_ids.add(current.id)
            current = db.query(TestcaseDirectory).get(current.pid) if current.pid else None

    # 3. 一次性查询所有相关节点
    all_nodes = db.query(TestcaseDirectory).filter(TestcaseDirectory.id.in_(node_ids)).all()
    nodes_dict = {node.id: node for node in all_nodes}

    # 4. 构建树形结构（前端需要的嵌套格式）
    def build_tree(node):
        return {
            "id": node.id,
            "pid": node.pid,
            "name": node.testDirectory_name,
            "children": [build_tree(child) for child in nodes_dict.values() if child.pid == node.id]
        }

    # 找到所有根节点（pid为None或不在当前节点集合中的）
    roots = [node for node in all_nodes if node.pid not in nodes_dict or node.pid is None]
    return [build_tree(root) for root in roots]