#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from collections import namedtuple, OrderedDict
import rules
import data

class Vehicle(object):

    def __init__(self, chassis, agent, computer, sensors_package, upgrade_list):
        self.chassis = chassis
        self.agent = agent
        self.computer = computer
        self.sensors_package = sensors_package
        self.upgrade_list = upgrade_list

        self.locomotion = ''
        self.weight = 0
        self.handling = 0
        self.max_speed = 0
        self.acceleration = 0
        self.load = 0
        self.used_load = 0
        self.capacity = 0
        self.used_capacity = 0
        self.size = 0
        self.constitution = 0
        self.armor = 0
        self.visibility = 0
        self.signature = 0
        self.sensors = []
        self.System = 0
        self.Processor = 0
        self.Firewall = 0
        self.Signal = 0
        self.Uplink = 0
        self.agent_rating = 0
        self.upgrades = []
        self.skills = {}

        self.structure = 0

        self.fill_initials()
        self.calc_stats()

    def fill_initials(self):
        self.weight = data.vehicle_chassis_dict[self.chassis].weight
        self.locomotion = data.vehicle_chassis_dict[self.chassis].locomotion
        self.handling = data.vehicle_chassis_dict[self.chassis].handling
        self.max_speed = data.vehicle_chassis_dict[self.chassis].max_speed
        self.acceleration = data.vehicle_chassis_dict[self.chassis].acceleration
        self.load = data.vehicle_chassis_dict[self.chassis].load
        self.capacity = data.vehicle_chassis_dict[self.chassis].capacity
        self.size = data.vehicle_chassis_dict[self.chassis].size
        self.constitution = data.vehicle_chassis_dict[self.chassis].constitution
        self.armor = data.vehicle_chassis_dict[self.chassis].armor
        self.visibility = data.vehicle_chassis_dict[self.chassis].visibility
        self.signature = data.vehicle_chassis_dict[self.chassis].signature
        self.cost = data.vehicle_chassis_dict[self.chassis].cost

        self.System = data.computer_dict[self.computer].System
        self.Processor = data.computer_dict[self.computer].Processor
        self.Signal = data.computer_dict[self.computer].Signal
        self.Uplink = data.computer_dict[self.computer].Uplink
        self.used_capacity += data.computer_dict[self.computer].Volume*1000
        self.used_load += data.computer_dict[self.computer].Volume*500
        self.cost += data.gameitems_dict[self.computer].cost

        self.agent_rating = data.agents_dict[self.agent].rating
        self.skills = data.agents_dict[self.agent].skills

        self.sensors = data.sensor_packages_dict[self.sensors_package].content
        for i in self.sensors:
            self.used_capacity += data.gameitems_dict[i].absolute_capacity
            self.used_load += data.gameitems_dict[i].weight
            self.cost += data.gameitems_dict[i].cost
        for upgrade in self.upgrade_list:
            upgrade = data.vehicle_upgrades_dict[upgrade]
            self.cost += upgrade.cost
            self.cost += upgrade.square_weight_cost * self.weight**0.5
            if isinstance(upgrade.capacity, str):
                self.used_capacity += eval('{}'.format(self.weight)+upgrade.capacity)
            else:
                self.used_capacity += upgrade.capacity
            if isinstance(upgrade.weight, str):
                self.used_load += eval('{}'.format(self.weight)+upgrade.weight)
            else:
                self.used_load += upgrade.weight
            self.upgrades.append(upgrade)

    def calc_stats(self):
        self.structure = rules.life(self.weight, self.constitution)
