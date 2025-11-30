<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;

class DiagnosticoService
{
    protected $url;

    public function __construct()
    {
        // URL del servicio de IA dentro de Docker
        $this->url = 'http://ia-diagnostico:8000/diagnostico';
    }

    public function generarDiagnostico(array $datos)
    {
        // Llamada POST a la IA con los datos
        $response = Http::post($this->url, $datos);

        if ($response->successful()) {
            return $response->json();
        }

        // Retorna error si no se pudo conectar
        return [
            'error' => 'No se pudo obtener el diagnóstico de la IA'
        ];
    }
}
