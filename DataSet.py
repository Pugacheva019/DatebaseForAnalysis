<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Dialog</string>
  </property>
  <widget class="QPushButton" name="datasetbutton">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>150</y>
     <width>171</width>
     <height>32</height>
    </rect>
   </property>
   <property name="text">
    <string>собрать датасет</string>
   </property>
  </widget>
  <widget class="QPushButton" name="downloadbutton">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>180</y>
     <width>171</width>
     <height>32</height>
    </rect>
   </property>
   <property name="text">
    <string>скачать контент</string>
   </property>
  </widget>
  <widget class="QPushButton" name="Postsbutton">
   <property name="geometry">
    <rect>
     <x>1</x>
     <y>210</y>
     <width>171</width>
     <height>32</height>
    </rect>
   </property>
   <property name="text">
    <string>ссылки на посты </string>
   </property>
  </widget>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>50</y>
     <width>211</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>Введите login пользователя</string>
   </property>
  </widget>
  <widget class="QTextEdit" name="textEdit">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>70</y>
     <width>161</width>
     <height>20</height>
    </rect>
   </property>
  </widget>
  <zorder>downloadbutton</zorder>
  <zorder>datasetbutton</zorder>
  <zorder>Postsbutton</zorder>
  <zorder>label</zorder>
  <zorder>textEdit</zorder>
 </widget>
 <resources/>
 <connections/>
</ui>
