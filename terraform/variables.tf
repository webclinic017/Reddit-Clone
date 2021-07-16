variable "region" {
    description = "Region to deploy resources into."
    type = string
    default = "us-east-1"
}

variable "availability_zones" {
    description = "availability zones in the aws region"
    type = list(string)
    default=["us-east-1a", "us-east-1b", "us-east-1c"]
}

// A boolean flag to enable/disable DNS support in the VPC.  Defaults true.
variable "vpc_dns_support" {
  description = "Should DNS support be enabled for the VPC?"
  type        = bool
  default     = true
}

// A boolean flag to enable/disable DNS hostnames in the VPC.  Defaults true.
variable "vpc_dns_hostnames" {
  description = "Should DNS hostnames support be enabled for the VPC?"
  type        = bool
  default     = true
}

variable "service_name" {
    type = string
    default = "app_service"
}

variable "auth_service_container_image" {
    type = string
}

variable "groups_service_container_image" {
    type = string
}

variable "posts_service_container_image" {
    type = string
}

variable "desired_capacity" {
    type = number
    default = 3
}

variable "min_capacity" {
    type = number
    default = 1
}

variable "max_capacity" {
    type = number
    default = 6
}

variable "instance_type" {
  description = "EC2 instance type for ECS launch configuration."
  type        = string
  default     = "t2.micro"
}

variable "ENV_USER_TABLE_NAME" {
    type = object({
        name = string
        value = string
    })
}

variable "ENV_TOKEN_TABLE_NAME" {
    type = object({
        name = string
        value = string
    })
}

variable "ENV_GROUPS_TABLE_NAME" {
    type = object({
        name = string
        value = string
    })
}

variable "ENV_MEMBERS_TABLE_NAME" {
    type = object({
        name = string
        value = string
    })
}

variable "ENV_POSTS_TABLE_NAME" {
    type = object({
        name = string
        value = string
    })
}

variable "ENV_RESPONSES_TABLE_NAME" {
    type = object({
        name = string
        value = string
    })
}

variable "ENV_AWS_REGION" {
    type = object({
        name = string
        value = string
    })
}

variable "ENV_TOKEN_PUBLIC_KEY" {
    description = "Environment variable for the public key used to sign auth tokens"
    type = object({
        name = string
        value = string
    })
    sensitive = true
}

variable "ENV_TOKEN_PRIVATE_KEY" {
    description = "Environment variable for the private key used to sign auth tokens"
    type = object({
        name = string
        value = string
    })
    sensitive = true
}
