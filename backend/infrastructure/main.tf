terraform {
  backend "local" {
    path = "./terraform.tfstate"
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_key_pair" "ec2_key" {
  key_name   = "insta-test-key"
  public_key = file("~/Downloads/insta-test.pem.pub")
}

resource "aws_security_group" "ec2_sg" {
  name        = "ec2-access-sg"
  description = "Allow SSH access"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "ec2_instance" {
  count         = var.instance_count
  ami           = "ami-0ec612e1caf93df8c"
  instance_type = var.instance_type
  key_name      = aws_key_pair.ec2_key.key_name
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = {
    Name = "ManagedInstance-${count.index}"
  }
}

variable "instance_type" {
  default = "t2.micro"
}

variable "instance_count" {
  default = 1
}

output "public_ips" {
  value = aws_instance.ec2_instance[*].public_ip
}