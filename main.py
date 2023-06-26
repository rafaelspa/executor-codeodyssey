import docker

docker_client = docker.from_env()

print('Is server responsive:')
print(docker_client.ping())

containers = docker_client.containers.list(all=True)
print('\nContainer list:')
for container in containers:
    print('ID: ', container.id)
    print('Name: ', container.name)
    print('Image: ', container.image)
    print('Status: ', container.status, '\n')
