
virt-install \
  --name archVM \
  --ram 1024 \
  --disk path=/data/vm/libvirt/images/archVM.qcow2,size=10 \
  --vcpus 1 \
  --os-type linux \
  --os-variant archlinux \
  --network bridge=virbr0 \
  --graphics none \
  --console pty,target_type=serial \
  --cdrom /data/vm/arch.iso \
  --noautoconsole
