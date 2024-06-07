import sys  
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog
from PyQt5.QtCore import QTimer
import sys, os

path = os.getcwd() + r'/src'
sys.path.append(path)

import pyfii as pf

class MainWindow(QWidget):  
    def __init__(self):  
        super().__init__()  
        self.initUI()  
  
    def initUI(self):  
        # 设置窗口标题和大小  
        self.setWindowTitle('PyFii')  
        self.setGeometry(100, 100, 400, 250)  
  
        # 创建布局  
        layout = QVBoxLayout()  
  
        # 输入文件路径  
        self.input_label = QLabel('输入文件：')  
        self.input_line_edit = QLineEdit()  
        layout.addWidget(self.input_label)  
        layout.addWidget(self.input_line_edit)  
  
        # 选择输入文件按钮  
        self.input_button = QPushButton('选择输入文件')  
        self.input_button.clicked.connect(self.select_input_file)  
        layout.addWidget(self.input_button)  
  
        # 输出文件路径  
        self.output_label = QLabel('输出文件：')  
        self.output_line_edit = QLineEdit()  
        layout.addWidget(self.output_label)  
        layout.addWidget(self.output_line_edit)  

        # 添加一个标签来显示状态信息  
        self.status_label = QLabel('')  
        layout.addWidget(self.status_label)  
  
        # 选择输出文件按钮（这里仅显示默认路径，用户可以手动编辑）  
        # 如果你想要一个文件选择对话框来选择输出文件，你可以添加一个按钮并连接到一个类似 select_input_file 的方法  
  
        # 添加间隔（可选）  
        #layout.addSpacing(20)  
  
        # 底部按钮  
        #self.settings_button = QPushButton('设置')  
        self.ok_button = QPushButton('确定') 
        self.ok_button.clicked.connect(self.on_ok_clicked)  # 连接信号到槽函数  
        layout.addWidget(self.ok_button)  
        self.exit_button = QPushButton('退出')  
        #layout.addWidget(self.settings_button)  
        layout.addWidget(self.ok_button)  
        layout.addWidget(self.exit_button)  
  
        # 连接退出按钮到关闭窗口的信号  
        self.exit_button.clicked.connect(self.close)  
  
        # 设置布局为窗口的布局  
        self.setLayout(layout)  
  
    def select_input_file(self):  
        # 打开文件选择对话框并获取选择的文件路径  
        input_file_path, _ = QFileDialog.getOpenFileName(self, '选择输入文件', "","Fii 文件 (*.fii)")  
        if input_file_path:  
            self.input_line_edit.setText(input_file_path)
            self.output_line_edit.setText(os.path.dirname(input_file_path)+".mp4")

    def on_ok_clicked(self):  
        # 获取输入和输出文件的路径  
        input_file_path = self.input_line_edit.text()  
        output_file_path = self.output_line_edit.text()  
          
        # 打印路径  
        print("输入文件路径:", input_file_path)  
        print("输出文件路径:", output_file_path)
        self.status_label.setText("视频生成中")
        QTimer.singleShot(1, self.on_video_generated)

    def on_video_generated(self):
        input_file_path = self.input_line_edit.text()  
        output_file_path = self.output_line_edit.text()  
        data,t0,music,feild,device=pf.read_fii(os.path.dirname(input_file_path),getdevice=True,fps=20,ignore_acc=False)
        pf.show(data,t0,music,feild=feild,device=device,save=os.path.splitext(output_file_path)[0],FPS=20,max_fps=20)
        self.status_label.setText("视频生成完成")  
  
if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    ex = MainWindow()  
    ex.show()  
    sys.exit(app.exec_())