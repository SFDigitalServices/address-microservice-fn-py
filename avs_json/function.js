{
    "scriptFile": "__init__.py",
    "bindings": [
      {
        "authLevel": "anonymous",
        "type": "httpTrigger",
        "direction": "in",
        "name": "req",
        "route": "avs/json",
        "methods": [
          "get"
        ]
      },
      {
        "type": "http",
        "direction": "out",
        "name": "$return"
      }
    ]
  }
  