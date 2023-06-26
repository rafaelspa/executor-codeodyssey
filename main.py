import docker

dockerClient = docker.from_env()

print('Container list')
containers = dockerClient.containers.list(all=True)
for container in containers:
    print(container.id)
    print(container.name)
    print(container.attrs)
