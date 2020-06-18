Vagrant.configure("2") do |config|
	config.vm.box = "ubuntu/bionic64"
	config.vm.network "private_network", ip: "192.168.33.12"
    config.vm.network "forwarded_port", guest: 5000, host: 5000
	config.vm.provider "virtualbox" do |vb|
		vb.memory = "2048"
	end
	config.vm.provision "history", type: "shell", inline: <<-SHELL
		echo '"\e[5~": history-search-backward' >> /home/vagrant/.inputrc
		echo '"\e[B":history-search-forward' >> /home/vagrant/.inputrc
		apt update
		apt install python3-pip
		pip3 install -r /vagrant/requirements.txt
		add-apt-repository -y ppa:flexiondotorg/audio
		apt-get -y install mp3gain
	SHELL
end