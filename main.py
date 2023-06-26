import docker

docker_client = docker.from_env()

print('Is server responsive:')
print(docker_client.ping())

images = docker_client.images.list(all=True)
print('\nImage list:')
for image in images:
    print('ID: ', image.id)
    print(f'Tags: ${image.tags}\n')

containers = docker_client.containers.list(all=True)
print('Container list:')
for container in containers:
    print('ID: ', container.id)
    print('Name: ', container.name)
    print('Image: ', container.image)
    print(f'Status: ${container.status}\n')
