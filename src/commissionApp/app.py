"""
My first application
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class commissionApp(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        #  the first app
        # main box
        main_box = toga.Box(style=Pack(direction=COLUMN))

        # 第 0 行 提示
        tips_label = toga.Label(
            text='提成点数为小数, 如0.18; 窗口费用提成之前扣除!',
            style=Pack(padding=(15, 0))
        )
        tips_box = toga.Box(style=Pack(direction=ROW, padding=5))
        tips_box.add(tips_label)

        # 第 1 行 提成点数
        deduct_label = toga.Label(
            text='提成点数：　',
            style=Pack(padding=(3, 5))
        )
        self.deduct_input = toga.TextInput(
            initial="0.18",
            style=Pack(flex=1)
            )
        deduct_box = toga.Box(style=Pack(direction=ROW, padding=5))
        deduct_box.add(deduct_label)
        deduct_box.add(self.deduct_input)

        # 第 2 行 窗口费用
        window_fee_label = toga.Label(
            text='窗口费用：　',
            style=Pack(padding=(3, 5))
        )
        self.window_fee_input = toga.TextInput(
            initial="0",
            style=Pack(flex=1)
            )
        window_fee_box = toga.Box(style=Pack(direction=ROW, padding=5))
        window_fee_box.add(window_fee_label)
        window_fee_box.add(self.window_fee_input)


        # 第 3 行 电费
        elect_label = toga.Label(
            text='电费：　　　',
            style=Pack(padding=(3, 5))
        )
        self.elect_input = toga.TextInput(
            initial="5000",
            style=Pack(flex=1)
            )
        elect_box = toga.Box(style=Pack(direction=ROW, padding=5))
        elect_box.add(elect_label)
        elect_box.add(self.elect_input)

        # 第 4 行 管理费
        manage_label = toga.Label(
            text='管理费用：　',
            style=Pack(padding=(3, 5))
        )
        self.manage_input = toga.TextInput(
            initial="7000",
            style=Pack(flex=1)
            )
        manage_box = toga.Box(style=Pack(direction=ROW, padding=5))
        manage_box.add(manage_label)
        manage_box.add(self.manage_input)

        # 第 5 行 营业额
        turnover_label = toga.Label(
            text='营业额：　　',
            style=Pack(padding=(3, 5))
        )
        self.turnover_input = toga.TextInput(
            initial="150000",
            style=Pack(flex=1)
            )
        turnover_box = toga.Box(style=Pack(direction=ROW, padding=5))
        turnover_box.add(turnover_label)
        turnover_box.add(self.turnover_input)

        # 按钮
        # 重置按钮
        reset_button = toga.Button(
            '重置',
            on_press=self.reset_fun,
            style=Pack(padding=5)
        )

        # 按钮
        cal_button = toga.Button(
            '计算',
            on_press=self.calculate_fun,
            style=Pack(padding=5)
        )

        btn_box = toga.Box(style=Pack(direction=ROW, padding=5))
        btn_box.add(reset_button)
        btn_box.add(cal_button)

        # 下面的 text 显示
        self.result_text = toga.MultilineTextInput(
            initial="计算得出: \n\n"
                    + "\t{} 点数提: {}\n".format(self.deduct_input.value, eval('(' + self.turnover_input.value + '-' + self.window_fee_input.value + ') *' + self.deduct_input.value))
                    + "\t窗口、电费、管理费共计: {}\n".format(eval(self.elect_input.value + '+' + self.manage_input.value + '+' + self.window_fee_input.value))
                    + "\t学校最终提点: {}\n".format(self.deduct_calculate_fun())
                    + "\n以上计算, 窗口费用不包含在提点范围内! \n",
            readonly=True,
            style=Pack(flex=1)
        )

        # 将上面的控件 逐个加入到主容器中
        main_box.add(tips_box)
        main_box.add(deduct_box)
        main_box.add(window_fee_box)
        main_box.add(elect_box)
        main_box.add(manage_box)
        main_box.add(turnover_box)
        main_box.add(btn_box)
        main_box.add(self.result_text)

        # 初始化窗口，配置主 Box
        #self.main_window_fee_dow.full_screen()
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        pass


    '''
        设置resultText结果
    '''
    def calculate_fun(self, widget):
        try:
            # 扣除提点
            deduct = float(self.deduct_input.value) 
            turnover = float(self.turnover_input.value)
            window_fee = float(self.window_fee_input.value)
            other  = float(eval(self.elect_input.value + '+' + self.manage_input.value))
            # 计算最终提点
            final_deduct = (deduct * (turnover - window_fee) + other + window_fee) / turnover

            self.result_text.value = (
                "计算得出: \n\n"
                + "\t{0} 点数提: {1}\n".format(deduct, deduct * (turnover - window_fee))
                + "\t窗口、电费、管理费共计: {}\n".format(other + window_fee)
                + "\t学校最终提点: {}\n".format(final_deduct)
                + "\t最终盈余: {}\n".format(turnover * (1 - final_deduct))
                + "\n以上计算, 窗口费用不包含在提点范围内! \n"
                )
        except ValueError:
            print('输入错误，提点为小数，其余为正数！\n')
            pass
        print(
            self.deduct_input.value
            , '\n', self.window_fee_input.value
            , '\n', self.elect_input.value
            , '\n', self.manage_input.value
            , '\n', self.turnover_input.value
            )
        pass


    '''
        计算最终提点数
    '''
    def deduct_calculate_fun(self) -> int:
        res = 0
        try:
            # 扣除提点
            deduct = float(self.deduct_input.value) 
            turnover = float(self.turnover_input.value)
            window_fee = float(self.window_fee_input.value)
            other  = float(eval(self.elect_input.value + '+' + self.manage_input.value))
            # 计算最终提点
            res = (deduct * (turnover - window_fee) + other + window_fee) / turnover
        except ValueError:
            print('输入错误，提点为小数，其余为正数！\n')
            pass
        print(
            self.deduct_input.value
            , '\n', self.window_fee_input.value
            , '\n', self.elect_input.value
            , '\n', self.manage_input.value
            , '\n', self.turnover_input.value
            )
        return res
    

    '''
        判断是否可以转换为 float
    '''
    def is_float(*str_float_list):
        try:
            # 因为使用float有一个例外是 'NaN'
            for strF in str_float_list:
                if strF == 'NaN':
                    return False
                float(strF)
            return True
        except ValueError:
            return False


    '''
        重置输入内容
    '''
    def reset_fun(self, widget):
        self.deduct_input.value = "0.18"
        self.window_fee_input.value = "0"
        self.elect_input.value = "5000"
        self.manage_input.value = "7000"
        self.turnover_input.value = "150000"


def main():
    return commissionApp()
