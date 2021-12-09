### FastApi example for use with Kubernetes and Vault dynamic secret

---



- Here we create a new Vault Role

```bash
vault write database/roles/sql-role... #omitted
```

- Using Agent Injector, there is a `vault.hashicorp.com/secret-volume-path` 
entry through which we can manage where to write the retrieved credentials into our apps

```yaml
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/agent-inject-status: "update"
        vault.hashicorp.com/role: "sql-role"
        vault.hashicorp.com/secret-volume-path: "/app/app/secrets/"
        vault.hashicorp.com/agent-inject-secret-.envapp: "database/creds/sql-role"
        vault.hashicorp.com/agent-inject-template-.envapp: |
          {{- with secret "database/creds/sql-role" -}}
          DB_USER={{ .Data.username }}
          DB_PASSWORD={{ .Data.password }}
          {{- end -}}
```

- When the vault rotates keys, we need the application to retrieve (using sidecar) and update into `/app/app/secrets/`

- Using the SqlAlchemy listeners, we will provide the new secrets when new connections are needed, 
for example when the pool changes.

```python
@event.listens_for(engine, "do_connect")
def receive_do_connect(dialect, conn_rec, cargs, cparams):
    print("opening new connections...")

    cparams["user"] = secrets.DB_USER
    cparams["password"] = secrets.DB_PASSWORD

    return psycopg2.connect(*cargs, **cparams)
```