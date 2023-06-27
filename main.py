import docker


def main():
    docker_client = docker.from_env()

    print('Is server responsive:')
    print(docker_client.ping())

    print("## Pulling nginx image")
    print(docker_client.images.pull('nginx'), '\n')

    images = docker_client.images.list(all=True)
    print('\nImage list:')
    for image in images:
        print('ID: ', image.id)
        print(f'Tags: ${image.tags}\n')

    print('## Container creation: client.containers.run("ubuntu:latest", "echo hello world")')
    print(docker_client.containers.run("ubuntu:latest", "echo hello world"), "\n")

    containers = docker_client.containers.list(all=True)
    print('Container list:')
    for container in containers:
        print('ID: ', container.id)
        print('Name: ', container.name)
        print('Image: ', container.image)
        print(f'Status: ${container.status}\n')

    optional_container = next((c for c in containers if 'whalesay-py' in c.name), None)
    print(optional_container)
    if not optional_container:
        print('Creating container whalesay-py . . .')
        created_container = docker_client.containers.create('docker/whalesay', command=['cowsay', 'hello there'],
                                                            name='whalesay-py')
        created_container.start()
        print('Container created and started')
        optional_container = created_container

    log_output = optional_container.logs(stream=True, stderr=True, stdout=True, timestamps=False, tail="all")
    for log in log_output:
        log_line = log.decode().rstrip()
        print(log_line)


if __name__ == "__main__":
    main()
