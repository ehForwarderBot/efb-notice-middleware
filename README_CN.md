
### 主要功能

- 在关闭消息通知的tg群组内，通过@来提醒
- 给微信消息添加 `#标签`，方便查找

### 使用  

`~/.ehforwarderbot/profiles/default/notice.NoticeMiddleware`目录下创建配置文件`config.yaml`  

```yaml
notices:
- 取件通知
- 超期提醒
- 取出通知
- 取件成功通知

tags:
- 取件通知
- 超期提醒:取件通知
```
