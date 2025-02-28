from sqlalchemy import text
from db.mysqldb import CustomSession


# 树形过滤
def selectByTreeTestCaseDirection(
        session: CustomSession,
        targetDirectoryName: str
):
    recursive_query = text("""
           WITH RECURSIVE filter_tree (id, pid, testDirectory_name) AS (
               SELECT id, pid, testDirectory_name
               FROM testcase_directory
               WHERE testDirectory_name LIKE :target_name

               UNION ALL

               SELECT t.id, t.pid, t.testDirectory_name
               FROM testcase_directory t
               INNER JOIN filter_tree ft ON ft.id = t.pid
           )
           SELECT DISTINCT id, pid, testDirectory_name FROM filter_tree;
       """)

    # 执行UPDATE语句
    with session() as s:  # 使用上下文管理器来确保会话正确关闭
        result = s.execute(recursive_query, {'target_name': f'%{targetDirectoryName}%'}).fetchall()

        # 将结果映射到 TestcaseDirectory 对象（可选，取决于您的需求）
        # 如果需要，您可以在这里添加代码来将每行结果转换为一个 TestcaseDirectory 实例
        # 但请注意，由于这是递归查询，直接映射到具有父子关系的对象可能比较复杂
        # 这里我们仅返回原始的行数据

    return result


