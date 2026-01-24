# 第一阶段：构建前端主题
FROM node:18-alpine AS frontend-builder

# 安装 git
RUN apk add --no-cache git

WORKDIR /build

# 克隆并构建 2024 主题
RUN git clone --depth 1 https://github.com/vastsa/FileCodeBoxFronted.git fronted-2024 && \
    cd fronted-2024 && \
    npm install && \
    npm run build

# 克隆并构建 2023 主题
RUN git clone --depth 1 https://github.com/vastsa/FileCodeBoxFronted2023.git fronted-2023 && \
    cd fronted-2023 && \
    npm install && \
    npm run build

# 第二阶段：构建最终镜像
FROM python:3.12-slim-bookworm
LABEL author="Lan"
LABEL email="xzu@live.com"

# 将当前目录下的文件复制到容器的 /app 目录
COPY . /app

# 设置时区为亚洲/上海
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

# 设置工作目录
WORKDIR /app

# 删除不必要的目录，减少镜像体积
RUN rm -rf docs fcb-fronted

# 从构建阶段复制编译好的前端主题
COPY --from=frontend-builder /build/fronted-2024/dist /app/themes/2024
COPY --from=frontend-builder /build/fronted-2023/dist /app/themes/2023

# 安装依赖
RUN pip install -r requirements.txt

# 暴露端口
EXPOSE 12345

# 启动应用
CMD ["python", "main.py"]