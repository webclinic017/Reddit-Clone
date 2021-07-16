locals {
  account_id = "${data.aws_caller_identity.current.account_id}"
}

//
// Create Roles
//

// Create roles for ECS services
resource "aws_iam_role" "ecs_service_role" {
  name               = "ecs_service_role"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.ecs_service_role_pd.json

  inline_policy {
    name = "ecs-service"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
            "elasticloadbalancing:DeregisterTargets",
            "elasticloadbalancing:Describe*",
            "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
            "elasticloadbalancing:RegisterTargets",
            "ec2:Describe*",
            "ec2:AuthorizeSecurityGroupIngress"
          ]
          Effect   = "Allow"
          Resource = "*"
        }
      ]
    })
  }
}

// Create role for EC2 instances that will run the ECS services
resource "aws_iam_role" "ec2_role" {
  name                = "ec2_role"
  path                = "/"
  assume_role_policy  = data.aws_iam_policy_document.ec2_role_pd.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"]

  inline_policy {
    name = "ecs-service"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "ec2:DescribeTags",
            "ecs:CreateCluster",
            "ecs:DeregisterContainerInstance",
            "ecs:DiscoverPollEndpoint",
            "ecs:Poll",
            "ecs:RegisterContainerInstance",
            "ecs:StartTelemetrySession",
            "ecs:UpdateContainerInstancesState",
            "ecs:Submit*"
          ]
          Effect   = "Allow"
          Resource = "*"
        }
      ]
    })
  }

  inline_policy {
    name = "dynamo-access"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "logs:CreateLogStream",
            "logs:PutLogEvents",
            "dynamodb:Query",
            "dynamodb:Scan",
            "dynamodb:GetItem",
            "dynamodb:PutItem",
            "dynamodb:UpdateItem",
            "dynamodb:DeleteItem"
          ]
          Effect   = "Allow"
          Resource = [
            "arn:aws:logs:us-east-1:${local.account_id}:*/*",
            "arn:aws:dynamodb:us-east-1:${local.account_id}:*/*"
          ]
        }
      ]
    })
  }

  inline_policy {
    name = "ecr-access"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "ecr:BatchCheckLayerAvailability",
            "ecr:BatchGetImage",
            "ecr:GetDownloadUrlForLayer",
            "ecr:GetAuthorizationToken"
          ]
          Effect   = "Allow"
          Resource = "*"
        }
      ]
    })
  }
}

// Create role for auto scaling groups
resource "aws_iam_role" "autoscaling_role" {
  name               = "autoscaling_role"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.autoscaling_pd.json

  inline_policy {
    name = "service-autoscaling"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action = [
            "ecs:DescribeServices",
            "ecs:UpdateService",
            "cloudwatch:PutMetricAlarm",
            "cloudwatch:DescribeAlarms",
            "cloudwatch:DeleteAlarms"
          ]
          Effect   = "Allow"
          Resource = [
            "arn:aws:ecs:us-east-1:${local.account_id}:*/*",
            "arn:aws:cloudwatch:us-east-1:${local.account_id}:*/*"
          ]
        }
      ]
    })
  }
}

//
// Create a new VPC
//
resource "aws_vpc" "prod_vpc" {
    cidr_block = "10.0.0.0/16"
    enable_dns_support   = var.vpc_dns_support
    enable_dns_hostnames = var.vpc_dns_hostnames

    tags = {
        Name = "Prod VPC"
    }
}

//
// Create an internet gateway for the VPC
//
resource "aws_internet_gateway" "prod_igw" {
    vpc_id = aws_vpc.prod_vpc.id

    tags = {
        Name = "Prod Internet Gateway"
    }
}

//
// Create 3 public subnets in the vpc
//
resource "aws_subnet" "public_subnet_1" {
    vpc_id = aws_vpc.prod_vpc.id
    cidr_block = "10.0.1.0/24"
    availability_zone = var.availability_zones[0]
    map_public_ip_on_launch = true

    tags = {
        Name = "Prod Public Subnet 1"
    }
}

resource "aws_subnet" "public_subnet_2" {
    vpc_id = aws_vpc.prod_vpc.id
    cidr_block = "10.0.2.0/24"
    availability_zone = var.availability_zones[1]
    map_public_ip_on_launch = true

    tags = {
        Name = "Prod Public Subnet 2"
    }
}

resource "aws_subnet" "public_subnet_3" {
    vpc_id = aws_vpc.prod_vpc.id
    cidr_block = "10.0.3.0/24"
    availability_zone = var.availability_zones[2]
    map_public_ip_on_launch = true

    tags = {
        Name = "Prod Public Subnet 3"
    }
}

//
// Create 3 private subnets in the vpc
//
resource "aws_subnet" "private_subnet_1" {
    vpc_id = aws_vpc.prod_vpc.id
    cidr_block = "10.0.4.0/24"
    availability_zone = var.availability_zones[0]

    tags = {
        Name = "Prod Private Subnet 1"
    }
}

resource "aws_subnet" "private_subnet_2" {
    vpc_id = aws_vpc.prod_vpc.id
    cidr_block = "10.0.5.0/24"
    availability_zone = var.availability_zones[1]

    tags = {
        Name = "Prod Private Subnet 2"
    }
}

resource "aws_subnet" "private_subnet_3" {
    vpc_id = aws_vpc.prod_vpc.id
    cidr_block = "10.0.6.0/24"
    availability_zone = var.availability_zones[2]

    tags = {
        Name = "Prod Private Subnet 3"
    }
}

//
// Create a NAT Gateway in each of the public subnets
//

// Need to create elastic IPs for NAT Gateways
resource "aws_eip" "nat_gateway_eip_1" {
    vpc = true
}

resource "aws_eip" "nat_gateway_eip_2" {
    vpc = true
}

resource "aws_eip" "nat_gateway_eip_3" {
    vpc = true
}

// Create Gateway 1
resource "aws_nat_gateway" "nat_gateway_1" {
    allocation_id = aws_eip.nat_gateway_eip_1.id
    subnet_id = aws_subnet.public_subnet_1.id

    depends_on = [
      aws_internet_gateway.prod_igw
    ]
}

// Create Gateway 2
resource "aws_nat_gateway" "nat_gateway_2" {
    allocation_id = aws_eip.nat_gateway_eip_2.id
    subnet_id = aws_subnet.public_subnet_2.id

    depends_on = [
      aws_internet_gateway.prod_igw
    ]
}

// Create Gateway 3
resource "aws_nat_gateway" "nat_gateway_3" {
    allocation_id = aws_eip.nat_gateway_eip_3.id
    subnet_id = aws_subnet.public_subnet_3.id

    depends_on = [
      aws_internet_gateway.prod_igw
    ]
}

//
// Create Route Table for the public subnet
//
resource "aws_route_table" "public_subnet_route_table" {
    vpc_id = aws_vpc.prod_vpc.id
}

resource "aws_route" "public" {
    route_table_id         = aws_route_table.public_subnet_route_table.id
    destination_cidr_block = "0.0.0.0/0"
    gateway_id             = aws_internet_gateway.prod_igw.id
}

resource "aws_route_table_association" "public_subnet_1" {
    subnet_id = aws_subnet.public_subnet_1.id
    route_table_id = aws_route_table.public_subnet_route_table.id
}

resource "aws_route_table_association" "public_subnet_2" {
    subnet_id = aws_subnet.public_subnet_2.id
    route_table_id = aws_route_table.public_subnet_route_table.id
}

resource "aws_route_table_association" "public_subnet_3" {
    subnet_id = aws_subnet.public_subnet_3.id
    route_table_id = aws_route_table.public_subnet_route_table.id
}

//
// Create Route tables for the two private subnets
//
resource "aws_route_table" "private_subnet_1_route_table" {
    vpc_id = aws_vpc.prod_vpc.id
}

resource "aws_route_table" "private_subnet_2_route_table" {
    vpc_id = aws_vpc.prod_vpc.id
}

resource "aws_route_table" "private_subnet_3_route_table" {
    vpc_id = aws_vpc.prod_vpc.id
}

resource "aws_route_table_association" "private_subnet_1" {
    subnet_id = aws_subnet.private_subnet_1.id
    route_table_id = aws_route_table.private_subnet_1_route_table.id
}

resource "aws_route_table_association" "private_subnet_2" {
    subnet_id = aws_subnet.private_subnet_2.id
    route_table_id = aws_route_table.private_subnet_2_route_table.id
}

resource "aws_route_table_association" "private_subnet_3" {
    subnet_id = aws_subnet.private_subnet_3.id
    route_table_id = aws_route_table.private_subnet_3_route_table.id
}

// All outbound traffic is directed to NAT Gateway
resource "aws_route" "private_1" {
    route_table_id = aws_route_table.private_subnet_1_route_table.id
    destination_cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway_1.id
}

// All outbound traffic is directed to NAT Gateway
resource "aws_route" "private_2" {
    route_table_id = aws_route_table.private_subnet_2_route_table.id
    destination_cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway_2.id
}

// All outbound traffic is directed to NAT Gateway
resource "aws_route" "private_3" {
    route_table_id = aws_route_table.private_subnet_3_route_table.id
    destination_cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway_3.id
}

//
// Network ACLs
//

// Create a public NACL.
resource "aws_network_acl" "public" {
  vpc_id = aws_vpc.prod_vpc.id
}

// Create the NACL rules for the public NACL.
resource "aws_network_acl_rule" "public_ingress" {
  network_acl_id = aws_network_acl.public.id
  rule_number    = 100
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
}

resource "aws_network_acl_rule" "public_egress" {
  network_acl_id = aws_network_acl.public.id
  rule_number    = 100
  egress         = true
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"

}

//
// Create a security group for http
//
resource "aws_security_group" "sg_allow_http" {
    name = "sg_allow_http"
    description = "Allow incoming HTTP"
    vpc_id = aws_vpc.prod_vpc.id

    ingress {
        description      = "Allow HTTP"
        from_port        = 80
        to_port          = 80
        protocol         = "tcp"
        cidr_blocks      = ["0.0.0.0/0"]
    }

    egress {
        from_port        = 0
        to_port          = 0
        protocol         = "-1"
        cidr_blocks      = ["0.0.0.0/0"]
    }

    tags = {
        Name = "allow_http"
    }
}

//
// Create a security group for https
//
resource "aws_security_group" "sg_allow_https" {
    name = "sg_allow_https"
    description = "Allow incoming HTTPS"
    vpc_id = aws_vpc.prod_vpc.id

    ingress {
        description      = "Allow HTTPS"
        from_port        = 443
        to_port          = 443
        protocol         = "tcp"
        cidr_blocks      = ["0.0.0.0/0"]
    }

    egress {
        from_port        = 0
        to_port          = 0
        protocol         = "-1"
        cidr_blocks      = ["0.0.0.0/0"]
    }

    tags = {
        Name = "allow_https"
    }
}

// Create a security group for the ALB.
resource "aws_security_group" "ecs_sg" {
  name        = "ecs-sg"
  description = "ECS security group for the ALB."
  vpc_id      = aws_vpc.prod_vpc.id

  ingress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol    = "tcp"
    from_port   = 8080
    to_port     = 8080
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol  = "tcp"
    from_port = 31000
    to_port   = 61000
    self      = true
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

//
// Create a Load Balancer for the EC2 instances
//
resource "aws_lb" "load_balancer" {
    name               = "load-balancer"
    internal           = false
    load_balancer_type = "application"
    idle_timeout               = 30
    enable_deletion_protection = false
    subnets            = [
                            aws_subnet.public_subnet_1.id,
                            aws_subnet.public_subnet_2.id,
                            aws_subnet.public_subnet_3.id
                        ]
    security_groups    = [aws_security_group.sg_allow_http.id,
                          aws_security_group.sg_allow_https.id,
                          aws_security_group.ecs_sg.id
                        ]
}

// create a target group for the auth service
resource "aws_lb_target_group" "auth_service_target_group" {
  name     = "auth-service-target-group"
  port     = 5000
  protocol = "HTTP"
  vpc_id   = aws_vpc.prod_vpc.id

  health_check {
    path                = "/api/v1/auth/public-key"
    protocol            = "HTTP"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 2
    interval            = 10
    matcher             = "200"
  }
}

// create a target group for the groups service
resource "aws_lb_target_group" "groups_service_target_group" {
  name     = "groups-service-target-group"
  port     = 5000
  protocol = "HTTP"
  vpc_id   = aws_vpc.prod_vpc.id

  health_check {
    path                = "/api/v1/groups/health-check"
    protocol            = "HTTP"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 2
    interval            = 10
    matcher             = "200"
  }
}

// create a target group for the posts service
resource "aws_lb_target_group" "posts_service_target_group" {
  name     = "posts-service-target-group"
  port     = 5000
  protocol = "HTTP"
  vpc_id   = aws_vpc.prod_vpc.id

  health_check {
    path                = "/api/v1/posts/health-check"
    protocol            = "HTTP"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 2
    interval            = 10
    matcher             = "200"
  }
}

// create a listener
resource "aws_lb_listener" "app_listener" {
  load_balancer_arn = aws_lb.load_balancer.arn
  port              = "80"
  protocol          = "HTTP"
  depends_on = [
    aws_lb.load_balancer
  ]

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.auth_service_target_group.arn
  }
}

// Create listener rule to forward traffic to the auth service
resource "aws_alb_listener_rule" "forward_to_auth" {
  listener_arn = aws_lb_listener.app_listener.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.auth_service_target_group.arn
  }

  condition {
    path_pattern {
      values = ["*/api/v1/auth/*"]
    }
  }
}

// Create listener rule to forward traffic to the groups service
resource "aws_alb_listener_rule" "forward_to_groups" {
  listener_arn = aws_lb_listener.app_listener.arn
  priority     = 95

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.groups_service_target_group.arn
  }

  condition {
    path_pattern {
      values = ["*/api/v1/groups", "*/api/v1/groups/*"]
    }
  }
}

// Create listener rule to forward traffic to the posts service
resource "aws_alb_listener_rule" "forward_to_posts" {
  listener_arn = aws_lb_listener.app_listener.arn
  priority     = 90

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.posts_service_target_group.arn
  }

  condition {
    path_pattern {
      values = ["*/api/v1/posts", "*/api/v1/posts/*"]
    }
  }
}


//
// ECS
//

// create a cluster for our application
resource "aws_ecs_cluster" "app_service_cluster" {
  name = "app-service-cluster"

  tags = {
    "Name" = "App Service Cluster"
  }
}

// create a service for the auth service
resource "aws_ecs_service" "auth_service" {
  name            = "auth-service"
  cluster         = aws_ecs_cluster.app_service_cluster.id
  task_definition = aws_ecs_task_definition.auth_service.arn
  desired_count   = 3
  iam_role        = aws_iam_role.ecs_service_role.arn
  depends_on      = [aws_lb_listener.app_listener]

  load_balancer {
    target_group_arn = aws_lb_target_group.auth_service_target_group.arn
    container_name   = "flask-auth-service"
    container_port   = 5000
  }
}

// define the auth service task
resource "aws_ecs_task_definition" "auth_service" {
  family                = "${var.service_name}-auth-service-app"
  container_definitions = <<DEFINITION
    [
      {
        "name": "flask-auth-service",
        "cpu": 10,
        "image": "${var.auth_service_container_image}",
        "essential": true,
        "memory": 300,
        "mountPoints": [
          {
            "containerPath": "/usr/local/apache2/htdocs",
            "sourceVolume": "my-vol"
          }
        ],
        "portMappings": [
          {
            "containerPort": 5000
          }
        ],
        "environment": [
          ${jsonencode(var.ENV_USER_TABLE_NAME)},
          ${jsonencode(var.ENV_TOKEN_TABLE_NAME)},
          ${jsonencode(var.ENV_TOKEN_PUBLIC_KEY)},
          ${jsonencode(var.ENV_TOKEN_PRIVATE_KEY)},
          ${jsonencode(var.ENV_AWS_REGION)}
        ]
      }
    ]
    DEFINITION
  volume {
    name = "my-vol"
  }
}

// create a service for the groups service
resource "aws_ecs_service" "groups_service" {
  name            = "groups-service"
  cluster         = aws_ecs_cluster.app_service_cluster.id
  task_definition = aws_ecs_task_definition.groups_service.arn
  desired_count   = 3
  iam_role        = aws_iam_role.ecs_service_role.arn
  depends_on      = [aws_lb_listener.app_listener]

  load_balancer {
    target_group_arn = aws_lb_target_group.groups_service_target_group.arn
    container_name   = "flask-groups-service"
    container_port   = 5000
  }
}

// define the groups service task
resource "aws_ecs_task_definition" "groups_service" {
  family                = "${var.service_name}-groups-service-app"
  container_definitions = <<DEFINITION
[
  {
    "name": "flask-groups-service",
    "cpu": 10,
    "image": "${var.groups_service_container_image}",
    "essential": true,
    "memory": 300,
    "mountPoints": [
      {
        "containerPath": "/usr/local/apache2/htdocs",
        "sourceVolume": "my-vol"
      }
    ],
    "portMappings": [
      {
        "containerPort": 5000
      }
    ],
    "environment": [
      ${jsonencode(var.ENV_GROUPS_TABLE_NAME)},
      ${jsonencode(var.ENV_MEMBERS_TABLE_NAME)},
      ${jsonencode(var.ENV_TOKEN_PUBLIC_KEY)},
      ${jsonencode(var.ENV_AWS_REGION)}
    ]
  }
]
DEFINITION
  volume {
    name = "my-vol"
  }
}

// create a service for the posts service
resource "aws_ecs_service" "posts_service" {
  name            = "posts-service"
  cluster         = aws_ecs_cluster.app_service_cluster.id
  task_definition = aws_ecs_task_definition.posts_service.arn
  desired_count   = 3
  iam_role        = aws_iam_role.ecs_service_role.arn
  depends_on      = [aws_lb_listener.app_listener]

  load_balancer {
    target_group_arn = aws_lb_target_group.posts_service_target_group.arn
    container_name   = "flask-posts-service"
    container_port   = 5000
  }
}

// define the posts service task
resource "aws_ecs_task_definition" "posts_service" {
  family                = "${var.service_name}-posts-service-app"
  container_definitions = <<DEFINITION
[
  {
    "name": "flask-posts-service",
    "cpu": 10,
    "image": "${var.posts_service_container_image}",
    "essential": true,
    "memory": 300,
    "mountPoints": [
      {
        "containerPath": "/usr/local/apache2/htdocs",
        "sourceVolume": "my-vol"
      }
    ],
    "portMappings": [
      {
        "containerPort": 5000
      }
    ],
    "environment": [
      {
        "name": "GROUPS_SERVICE_URL",
        "value": "${aws_lb.load_balancer.dns_name}"
      },
      ${jsonencode(var.ENV_POSTS_TABLE_NAME)},
      ${jsonencode(var.ENV_RESPONSES_TABLE_NAME)},
      ${jsonencode(var.ENV_TOKEN_PUBLIC_KEY)},
      ${jsonencode(var.ENV_AWS_REGION)}
    ]
  }
]
DEFINITION
  volume {
    name = "my-vol"
  }
}

// Create an EC2 instance profile.
resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "ec2_instance_profile"
  role = aws_iam_role.ec2_role.name
}

// Create an EC2 Launch Configuration for the ECS cluster.
resource "aws_launch_configuration" "ecs_launch_config" {
  image_id             = data.aws_ami.latest_ecs_ami.image_id
  security_groups      = [aws_security_group.sg_allow_http.id, aws_security_group.sg_allow_https.id, aws_security_group.ecs_sg.id]
  instance_type        = var.instance_type
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name
  user_data            = "#!/bin/bash\necho ECS_CLUSTER=app-service-cluster >> /etc/ecs/ecs.config"
}

// Create the ECS autoscaling group.
resource "aws_autoscaling_group" "ecs_asg" {
  name                 = "ecs-asg"
  vpc_zone_identifier  = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id, aws_subnet.private_subnet_3.id]
  launch_configuration = aws_launch_configuration.ecs_launch_config.name

  desired_capacity = var.desired_capacity
  min_size         = var.min_capacity
  max_size         = var.max_capacity
}

// Create an autoscaling policy.
resource "aws_autoscaling_policy" "ecs_infra_scale_out_policy" {
  name                   = "ecs_infra_scale_out_policy"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  autoscaling_group_name = aws_autoscaling_group.ecs_asg.name
}

// Create an application autoscaling target for auth service.
resource "aws_appautoscaling_target" "auth_ecs_service_scaling_target" {
  max_capacity       = 5
  min_capacity       = 2
  resource_id        = "service/${aws_ecs_cluster.app_service_cluster.name}/auth-service"
  scalable_dimension = "ecs:service:DesiredCount"
  role_arn           = aws_iam_role.autoscaling_role.arn
  service_namespace  = "ecs"
  depends_on         = [aws_ecs_service.auth_service]
}

// Create an application autoscaling target for groups service.
resource "aws_appautoscaling_target" "groups_ecs_service_scaling_target" {
  max_capacity       = 5
  min_capacity       = 2
  resource_id        = "service/${aws_ecs_cluster.app_service_cluster.name}/groups-service"
  scalable_dimension = "ecs:service:DesiredCount"
  role_arn           = aws_iam_role.autoscaling_role.arn
  service_namespace  = "ecs"
  depends_on         = [aws_ecs_service.groups_service]
}

// Create an application autoscaling target for posts service.
resource "aws_appautoscaling_target" "posts_ecs_service_scaling_target" {
  max_capacity       = 5
  min_capacity       = 2
  resource_id        = "service/${aws_ecs_cluster.app_service_cluster.name}/posts-service"
  scalable_dimension = "ecs:service:DesiredCount"
  role_arn           = aws_iam_role.autoscaling_role.arn
  service_namespace  = "ecs"
  depends_on         = [aws_ecs_service.posts_service]
}

// Create an ECS service CPU target tracking scale out policy.
resource "aws_appautoscaling_policy" "auth_ecs_service_cpu_scale_out_policy" {
  name               = "cpu-target-tracking-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.auth_ecs_service_scaling_target.resource_id
  scalable_dimension = aws_appautoscaling_target.auth_ecs_service_scaling_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.auth_ecs_service_scaling_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value       = 50.0
    scale_in_cooldown  = 60
    scale_out_cooldown = 60
  }
}

// Create an ECS service CPU target tracking scale out policy.
resource "aws_appautoscaling_policy" "groups_ecs_service_cpu_scale_out_policy" {
  name               = "cpu-target-tracking-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.groups_ecs_service_scaling_target.resource_id
  scalable_dimension = aws_appautoscaling_target.groups_ecs_service_scaling_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.groups_ecs_service_scaling_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value       = 50.0
    scale_in_cooldown  = 60
    scale_out_cooldown = 60
  }
}

// Create an ECS service CPU target tracking scale out policy.
resource "aws_appautoscaling_policy" "posts_ecs_service_cpu_scale_out_policy" {
  name               = "cpu-target-tracking-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.posts_ecs_service_scaling_target.resource_id
  scalable_dimension = aws_appautoscaling_target.posts_ecs_service_scaling_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.posts_ecs_service_scaling_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value       = 50.0
    scale_in_cooldown  = 60
    scale_out_cooldown = 60
  }
}
