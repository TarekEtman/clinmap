import { Suspense, useMemo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function ParticleField() {
  const ref = useRef<THREE.Points>(null);
  const positions = useMemo(() => {
    const count = 1100;
    const arr = new Float32Array(count * 3);
    for (let i = 0; i < count; i += 1) {
      const radius = 4 + Math.random() * 8;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(THREE.MathUtils.randFloatSpread(2));
      arr[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      arr[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta) * 0.55;
      arr[i * 3 + 2] = radius * Math.cos(phi) - 2;
    }
    return arr;
  }, []);

  useFrame(({ clock }) => {
    if (!ref.current) return;
    ref.current.rotation.y = clock.elapsedTime * 0.025;
    ref.current.rotation.x = Math.sin(clock.elapsedTime * 0.18) * 0.04;
  });

  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" count={positions.length / 3} array={positions} itemSize={3} />
      </bufferGeometry>
      <pointsMaterial size={0.018} color="#6F7A82" transparent opacity={0.32} sizeAttenuation />
    </points>
  );
}

function OrbitRing({ radius, color, speed, rotation }: { radius: number; color: string; speed: number; rotation: [number, number, number] }) {
  const ref = useRef<THREE.Mesh>(null);
  useFrame(({ clock }) => {
    if (!ref.current) return;
    ref.current.rotation.z = clock.elapsedTime * speed;
    ref.current.rotation.x = rotation[0] + Math.sin(clock.elapsedTime * 0.25) * 0.04;
  });
  return (
    <mesh ref={ref} rotation={rotation} position={[0, 0, -1.2]}>
      <torusGeometry args={[radius, 0.01, 12, 192]} />
      <meshBasicMaterial color={color} transparent opacity={0.42} />
    </mesh>
  );
}

function FloatingPanel({ position, rotation, scale }: { position: [number, number, number]; rotation: [number, number, number]; scale: [number, number, number] }) {
  const ref = useRef<THREE.Mesh>(null);
  useFrame(({ clock }) => {
    if (!ref.current) return;
    ref.current.position.y = position[1] + Math.sin(clock.elapsedTime * 0.8 + position[0]) * 0.08;
  });
  return (
    <mesh ref={ref} position={position} rotation={rotation} scale={scale}>
      <boxGeometry args={[1.2, 0.72, 0.025]} />
      <meshStandardMaterial color="#EEF0EC" emissive="#A95132" emissiveIntensity={0.06} roughness={0.35} metalness={0.5} transparent opacity={0.42} />
    </mesh>
  );
}

export default function LabScene() {
  return (
    <Canvas camera={{ position: [0, 0, 7.2], fov: 45 }} dpr={[1, 1.7]} gl={{ antialias: true, alpha: true }}>
      <ambientLight intensity={0.45} />
      <pointLight position={[-4, 3, 4]} intensity={0.95} color="#A95132" />
      <pointLight position={[4, -2, 3]} intensity={0.8} color="#0E2630" />
      <pointLight position={[0, 4, 2]} intensity={0.55} color="#F7F4EF" />
      <Suspense fallback={null}>
        <ParticleField />
        <OrbitRing radius={2.15} color="#A95132" speed={0.12} rotation={[1.15, 0.22, 0.2]} />
        <OrbitRing radius={2.7} color="#303846" speed={-0.08} rotation={[1.35, -0.5, 1.1]} />
        <OrbitRing radius={3.25} color="#0E2630" speed={0.055} rotation={[1.1, 0.75, -0.6]} />
        <FloatingPanel position={[-3.2, 1.4, -2.2]} rotation={[0.25, 0.75, 0.08]} scale={[0.9, 0.9, 0.9]} />
        <FloatingPanel position={[3.25, 0.55, -2.6]} rotation={[-0.15, -0.82, -0.08]} scale={[1.05, 1.05, 1.05]} />
        <FloatingPanel position={[2.4, -1.75, -2.9]} rotation={[0.15, -0.55, 0.12]} scale={[0.72, 0.72, 0.72]} />
      </Suspense>
    </Canvas>
  );
}
