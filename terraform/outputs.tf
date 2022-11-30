resource "random_pet" "image" {}

output "IMAGE_NAME" {
    value = random_pet.image.id
}
