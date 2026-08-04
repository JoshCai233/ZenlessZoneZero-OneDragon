from one_dragon.base.operation.application import application_const
from one_dragon.base.operation.operation_edge import node_from
from one_dragon.base.operation.operation_node import operation_node
from one_dragon.base.operation.operation_notify import node_notify, NotifyTiming
from one_dragon.base.operation.operation_round_result import OperationRoundResult
from one_dragon.base.screen import screen_utils
from typing import List, Optional
from zzz_od.application.test import test_const
from zzz_od.application.test.test_run_record import (
    TestRunRecord,
)
from zzz_od.application.zzz_application import ZApplication
from zzz_od.context.zzz_context import ZContext


class TestApp(ZApplication):

    def __init__(self, ctx: ZContext):
        """
        兑换码兑换
        """
        ZApplication.__init__(
            self,
            ctx=ctx,
            app_id=test_const.APP_ID,
            op_name=test_const.APP_NAME,
        )
        self.run_record: Optional[TestRunRecord] = self.ctx.run_context.get_run_record(
            app_id=test_const.APP_ID,
            instance_idx=self.ctx.current_instance_idx,
        )

        self.unused_code_list: List[str] = []
        self.code_idx: int = 0  # 当前输入兑换码的下标

    def handle_init(self) -> None:
        """
        执行前的初始化 由子类实现
        注意初始化要全面 方便一个指令重复使用
        """
        pass

    @operation_node(name='node1', is_start_node=True)
    @node_notify(when=NotifyTiming.CURRENT_SUCCESS)
    def node1(self) -> OperationRoundResult:
        agent_area = self.ctx.screen_loader.get_area('迷失之地-矩阵行动-编队选择', '代理人列表')
        screen_utils.scroll_area(self.ctx, agent_area, 'down', 0.75, 0.25)
        screen_utils.scroll_area(self.ctx, agent_area, 'up', 0.75, 0.25)
        return self.round_retry()

    @node_from(from_name='node1')
    @operation_node(name='node2')
    @node_notify(when=NotifyTiming.CURRENT_DONE)
    def node2(self) -> OperationRoundResult:
        return self.round_success()

    @node_from(from_name='node2')
    @operation_node(name='node3')
    @node_notify(when=NotifyTiming.CURRENT_DONE)
    def node3(self) -> OperationRoundResult:
        return self.round_success()


def __debug():
    ctx = ZContext()
    ctx.init()
    ctx.run_context.run_application(
        app_id=test_const.APP_ID,
        instance_idx=ctx.current_instance_idx,
        group_id=application_const.DEFAULT_GROUP_ID,
    )


if __name__ == '__main__':
    __debug()
