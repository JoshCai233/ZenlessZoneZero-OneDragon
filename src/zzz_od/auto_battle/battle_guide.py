import time

from zzz_od.operation.zzz_operation import ZOperation


def check_battle_guide(app: ZOperation) -> None:
    """
    判断是否在战斗引导中， 如果是的话就点5次下一页然后关闭
    """
    area = app.ctx.screen_loader.get_area('委托助手', '玩法引导')
    ocr_result_list = app.ctx.ocr_service.get_ocr_result_list(image=app.last_screenshot, rect=area.rect)
    for mr in ocr_result_list:
        if mr.data == '战斗引导':
            for i in range(5):
                app.round_by_find_and_click_area(app.screenshot(), '委托助手', '按钮-下一页')
                time.sleep(1)
            app.round_by_find_and_click_area(app.screenshot(), '委托助手', '按钮-战斗引导-关闭')
