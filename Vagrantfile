Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/eoan64"
   config.vm.boot_timeout = 600
   config.ssh.insert_key = true
   config.vm.provision "shell", inline: <<-SHELL
    #ENVIRONMENT
    sudo echo "LANG=en_US.UTF-8" >> /etc/environment
    sudo echo "LANGUAGE=en_US.UTF-8" >> /etc/environment
    sudo echo "LC_ALL=en_US.UTF-8" >> /etc/environment
    sudo echo "LC_CTYPE=en_US.UTF-8" >> /etc/environment
    #REPOSITORIES
    sudo apt-get update
    sudo apt-get -y upgrade
    #g++, git, curl...
    echo "installing g++..."
    sudo apt-get install -y g++
    echo "installing GIT..."
    sudo apt-get install -y git
    echo "installing CURL..."
    sudo apt-get install -y curl
     apt-get install python-opencv
    #conda
    echo "conda tinamica version"

    curl -LO http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    sudo bash Miniconda3-latest-Linux-x86_64.sh -b -p /home/vagrant/miniconda
    export PATH="/home/vagrant/miniconda/bin:$PATH"
    echo 'export PATH="/home/vagrant/miniconda/bin:$PATH"' >> /home/vagrant/.bashrc
    conda create -n tinamica --clone="/home/vagrant/miniconda"
    source activate tinamica
	conda update -y conda
	conda upgrade -y conda
	conda install -c anaconda -y python=3.6 && \
    conda install \
    pillow=6.2.1 \
    pandas=0.25.3 \
    tensorflow=1.14 \
    numpy=1.17
    conda install -c anaconda -y protobuf=3.8 && \
    conda install -y Cython && \
    conda install -y matplotlib
  SHELL
   config.vm.provider "virtualbox" do |vb|
     vb.memory = 6144
     vb.cpus = 2
     vb.name = "tinnamica-dev"
  end

end