# resource "azurerm_resource_group" "rg" {
#   name     = "humanitec-workshop"
#   location = var.location

#   tags = {
#     environment = "dev"
#   }
# }

# resource "azurerm_virtual_network" "vnet" {
#   name                = "humanitec-vnet"
#   location            = azurerm_resource_group.rg.location
#   address_space       = [var.address_space]
#   resource_group_name = azurerm_resource_group.rg.name
# }

# resource "azurerm_subnet" "subnet" {
#   name                 = "humanitec-subnet"
#   virtual_network_name = azurerm_virtual_network.vnet.name
#   resource_group_name  = azurerm_resource_group.rg.name
#   address_prefixes     = [var.subnet_prefix]
# }

# resource "azurerm_kubernetes_cluster" "humanitec" {
#   name                = "aks-humanitec"
#   location            = azurerm_resource_group.rg.location
#   resource_group_name = azurerm_resource_group.rg.name
#   dns_prefix          = "exampleaks1"

#   default_node_pool {
#     name       = "default"
#     node_count = 1
#     vm_size    = "Standard_D2_v2"
#   }

#   identity {
#     type = "SystemAssigned"
#   }

#   tags = {
#     Environment = "dev"
#   }
# }

# variable "location" {
#   description = "The region where the virtual network is created."
#   default     = "centralus"
# }

# variable "address_space" {
#   description = "The address space that is used by the virtual network. You can supply more than one address space. Changing this forces a new resource to be created."
#   default     = "10.0.0.0/16"
# }

# variable "subnet_prefix" {
#   description = "The address prefix to use for the subnet."
#   default     = "10.0.10.0/24"
# }


# output "aks_endpoint" {
#     value = azurerm_kubernetes_cluster.humanitec.fqdn
# }

