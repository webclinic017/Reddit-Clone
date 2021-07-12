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

variable "auth-service-container-image" {
    type = string
    default = "692775535794.dkr.ecr.us-east-1.amazonaws.com/flask-auth-service"
}

variable "groups-service-container-image" {
    type = string
    default = "692775535794.dkr.ecr.us-east-1.amazonaws.com/flask-groups-service"
}

variable "posts-service-container-image" {
    type = string
    default = "692775535794.dkr.ecr.us-east-1.amazonaws.com/flask-posts-service"
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

variable "instance_ami" {
    type = string
    default = "ami-0ab4d1e9cf9a1215a"
}