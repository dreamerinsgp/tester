# CI/CD 冒烟测试演示

独立的 CI/CD 演示项目，用于展示：**构建镜像 → 推送到 Docker Hub → 部署到 K8s → 跑冒烟测试** 的完整流程。

与 dex_full 仓库无关，可单独推送到任意 Git 仓库（如 `tester` 或 `cicd-smoke-demo`）。

## 结构

```
cicd-smoke-demo/
├── Jenkinsfile          # Pipeline 定义
├── demo_server/         # 待部署的 Flask API
├── k8s/                 # K8s 清单
└── api_auto/            # 冒烟测试
```

## 快速开始

### 1. 推送到 Git 仓库

```bash
cd cicd-smoke-demo
git init
git add .
git commit -m "init: CI/CD smoke demo"
git remote add origin https://github.com/你的用户名/tester.git
git push -u origin main
```

### 2. Jenkins 配置

- 新建 Pipeline 任务
- **Repository URL**：上面推送的仓库地址
- **Script Path**：`Jenkinsfile`
- 添加凭据 `docker-hub`（Docker Hub 用户名 + Access Token）
- 确保 `~/.jenkins/kubeconfig` 可访问 K8s

### 3. 运行

点击 **Build Now** 触发完整流程。
